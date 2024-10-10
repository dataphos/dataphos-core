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

from pulumi import ResourceOptions
from pulumi_gcp import organizations, pubsub

from infrastructure.ResourceCreator import ResourceCreator
from infrastructure.broker.AbstractMessageBroker import AbstractMessageBroker
import infrastructure.broker.pubsub.pubsub_config as pubsub_config
from config import resource_tags


class PubSubMessageBroker(AbstractMessageBroker):

    def __init__(self, broker_id: str, broker_config: dict, project: organizations.Project, parent) -> None:
        self._parent = parent
        self._project_id = project.project_id

        self.project_id = broker_config["projectID"]
        self.topics = {}
        self.subscriptions = {}

    # interface methods
    def add_topic(self, topic_name: str, topic_config: dict):
        topic_data = self._get_topic(topic_name)

        if resource_tags and not topic_config.get("labels"):
            topic_config["labels"] = resource_tags

        opts = ResourceOptions(parent=self._parent)
        topic = self.create_or_import_resource(topic_name, pubsub_config.topic_properties, topic_config, topic_data, opts, self._create_topic)
        self.topics[topic_name] = topic
        self.subscriptions[topic_name] = {}
        return topic

    def add_subscription(self, topic_name: str, subscription_name: str, subscription_config: dict):
        subscription_data = self._get_subscription(subscription_name)

        if resource_tags and not subscription_config.get("labels"):
            subscription_config["labels"] = resource_tags

        topic = self.topics[topic_name]
        opts = ResourceOptions(parent=topic)
        subscription = self.create_or_import_resource(subscription_name, pubsub_config.subscription_properties, subscription_config, subscription_data, opts, self._create_subscription)
        self.subscriptions[topic_name][subscription_name] = subscription
        return subscription

    def export_config(self) -> dict:
        platform_config = {
            "projectID": self.project_id,
        }
        return platform_config

    # internal methods
    def _get_topic(self, topic_name: str) -> pubsub.Topic:
        try:
            topic_data = pubsub.get_topic(
                name=topic_name,
                project=self.project_id
            )
        except:
            topic_data = None
        return topic_data

    def _create_topic(self, topic_name: str, topic_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> pubsub.Topic:
        return pubsub.Topic(
            topic_name,
            name=topic_name,
            project=self._project_id,
            message_retention_duration=topic_config.message_retention_duration,
            schema_settings=pubsub.TopicSchemaSettingsArgs(
                schema=topic_config.schema_settings[0].get("schema"),
                encoding=topic_config.schema_settings[0].get("encoding"),
            ) if topic_config.schema_settings and topic_config.schema_settings[0].get("schema") else None,
            kms_key_name=None,
            message_storage_policy=None,
            labels=topic_config.labels,
            opts=opts
        )

    def _get_subscription(self, subscription_name: str) -> pubsub.subscription:
        try:
            subscription_data = pubsub.get_subscription(
                name=subscription_name,
                project=self.project_id
            )
        except:
            subscription_data = None
        return subscription_data

    def _create_subscription(self, subscription_name: str, subscription_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> pubsub.Subscription:
        topic_name = opts.parent._name

        push_endpoint = None
        if subscription_config.push_configs:
            push_config = subscription_config.push_configs[0]
            push_host = push_config.get("host")
            push_endpoint = f"https://{push_host}/push" if push_host else push_config.get("push_endpoint")

        return pubsub.Subscription(
            f"{topic_name}-{subscription_name}",
            name=subscription_name,
            topic=topic_name,
            project=self._project_id,
            retain_acked_messages=subscription_config.retain_acked_messages,
            enable_message_ordering=subscription_config.enable_message_ordering,
            retry_policy=pubsub.SubscriptionRetryPolicyArgs(
                minimum_backoff=subscription_config.retry_policies[0].get("minimum_backoff"),
                maximum_backoff=subscription_config.retry_policies[0].get("maximum_backoff"),
            ) if subscription_config.retry_policies else None,
            push_config=pubsub.SubscriptionPushConfigArgs(
                push_endpoint=push_endpoint,
            ) if push_endpoint else None,
            labels=subscription_config.labels,
            opts=opts
        )
