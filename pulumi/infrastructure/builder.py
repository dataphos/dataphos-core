# Copyright 2024 Syntio Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from infrastructure.platform.Platform import Platform
from infrastructure.cluster.KubernetesCluster import KubernetesCluster
from infrastructure.broker.MessageBroker import MessageBroker
from infrastructure.storage.Storage import Storage
from infrastructure.accounts.Account import Account

platform = Platform()


def create_cluster(cluster_map):
    cluster_id, cluster_config = list(cluster_map.items())[0]
    cluster = KubernetesCluster(cluster_id, cluster_config, platform)
    kubernetes_provider = cluster.get_kubernetes_provider()
    platform.set_kubernetes_provider(kubernetes_provider)
    return kubernetes_provider


def create_storage(storage_map):
    storage_resources = {}
    exported_config = {}

    for storage_id, storage_config in storage_map.items():
        storage = Storage(storage_id, storage_config, platform)

        buckets = storage_config.get("buckets", {})
        for bucket_name, bucket_config in buckets.items():
            storage.add_bucket(bucket_name, bucket_config)

        storage.register_outputs({})

        storage_resources[storage_id] = storage.get_instance()
        exported_config[storage_id] = storage.export_config()

    return storage_resources, exported_config


def create_brokers(brokers_map):
    broker_resources = {}
    exported_config = {}

    for broker_id, broker_config in brokers_map.items():
        broker = MessageBroker(broker_id, broker_config, platform)

        topics = broker_config.get("topics", {})
        for topic_name, topic_config in topics.items():
            broker.add_topic(topic_name, topic_config)

            subscriptions = topic_config.get("subscriptions", {})
            for subscription_name, subscription_config in subscriptions.items():
                broker.add_subscription(topic_name, subscription_name, subscription_config)

        broker.register_outputs({})

        broker_resources[broker_id] = broker.get_instance()
        exported_config[broker_id] = broker.export_config()

    return broker_resources, exported_config


def create_accounts(accounts_map, broker_resources, storage_resources):
    exported_config = {}

    for app_id, account_config in accounts_map.items():
        exported_config[app_id] = {}
        account = Account(app_id, account_config, platform)
        exported_config[app_id].update(account.export_config())

        for role_config in account_config["roles"]:
            broker = role_config.get("broker")
            if broker:
                account.add_broker_role(broker_resources[broker], role_config)
                continue
            storage = role_config.get("storage")
            if storage:
                account.add_storage_role(storage_resources[storage], role_config)

        account.register_outputs({})

    return exported_config
