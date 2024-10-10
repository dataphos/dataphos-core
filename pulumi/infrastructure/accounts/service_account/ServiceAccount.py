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

from pulumi import ResourceOptions, Output
from pulumi_gcp import organizations, projects, serviceaccount
from pulumi_gcp.pubsub import TopicIAMMember, SubscriptionIAMMember
from pulumi_gcp.storage import BucketIAMMember

from infrastructure.broker.pubsub.PubSubMessageBroker import PubSubMessageBroker
from infrastructure.storage.gcs.GoogleCloudStorage import GoogleCloudStorage
from infrastructure.accounts.AbstractAccount import AbstractAccount
from infrastructure.accounts.AccountRoleScope import AccountRoleScope
import infrastructure.accounts.service_account.service_account_config as config


class ServiceAccount(AbstractAccount):
    def __init__(self, app_id: str, project: organizations.Project, parent):
        self._parent = parent
        self._app_id = app_id
        self._service_account_id = f"{app_id}-sa"
        self._service_account, self._private_key = self._create_service_account(self._service_account_id, project.project_id)
        self._sa_email = self._service_account.email

    # interface methods
    def add_broker_role(self, broker: PubSubMessageBroker, role_config: dict):
        role_definition = config.ROLE_DEFINITIONS[role_config["roleID"]]

        if role_config["scope"] == AccountRoleScope.PROJECT:
            return self._add_project_role(broker, role_definition)

        role_name = role_definition["name"]
        role_id = role_definition["id"]

        topic_name = role_config["topic"]
        topic = broker.topics[topic_name]
        opts = ResourceOptions(parent=self._service_account)
        TopicIAMMember(
            f"{self._app_id}-{topic_name}-{role_name}",
            project=broker.project_id,
            topic=topic.name,
            role=role_id,
            member=Output.format("serviceAccount:{0}", self._sa_email),
            opts=opts
        )

        subscription_name = role_config.get("consumerID")
        if not subscription_name: return

        subscription = broker.subscriptions[topic_name][subscription_name]
        opts = ResourceOptions(parent=self._service_account)
        SubscriptionIAMMember(
            f"{self._app_id}-{subscription_name}-{role_definition['name']}",
            project=broker.project_id,
            subscription=subscription.name,
            role=role_definition['id'],
            member=Output.format("serviceAccount:{0}", self._sa_email),
            opts=opts
        )

    def add_storage_role(self, storage: GoogleCloudStorage, role_config: dict):
        role_definition = config.ROLE_DEFINITIONS[role_config["roleID"]]

        if role_config["scope"] == AccountRoleScope.PROJECT:
            return self._add_project_role(storage, role_definition)

        bucket_name = role_config["storageTargetID"]
        bucket = storage.buckets[bucket_name]
        opts = ResourceOptions(parent=self._service_account)
        BucketIAMMember(
            f"{self._app_id}-{bucket_name}-{role_definition['name']}",
            bucket=bucket.name,
            role=role_definition['id'],
            member=Output.format("serviceAccount:{0}", self._sa_email),
            opts=opts
        )

    def export_config(self):
        account_config = {
            "serviceAccountSecret": f"{self._app_id}-gcp-sa-key",
            "serviceAccountKey": self._private_key,
        }
        return account_config

    # internal methods
    def _create_service_account(self, service_account_id, project_id):
        account_description = f"Grants {self._app_id} required permissions for PubSub and GCS."
        service_account = serviceaccount.Account(service_account_id,
            account_id=service_account_id,
            display_name=service_account_id,
            description=account_description,
            project=project_id,
            opts=ResourceOptions(parent=self._parent)
        )

        sa_key = serviceaccount.Key(
            f"{service_account_id}-key",
            service_account_id=service_account.email,
            opts=ResourceOptions(parent=service_account)
        )
        private_key = sa_key.private_key
        return service_account, private_key

    def _add_project_role(self, resource, role_definition: dict):
        opts = ResourceOptions(parent=self._service_account)
        projects.IAMMember(
            f"{self._app_id}-{resource.project_id}-{role_definition['name']}",
            project=resource.project_id,
            role=role_definition['id'],
            member=Output.format("serviceAccount:{0}", self._sa_email),
            opts=opts
        )
