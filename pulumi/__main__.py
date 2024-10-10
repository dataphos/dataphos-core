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

from pulumi.resource import ResourceOptions
import pulumi_kubernetes as kubernetes
from pulumi_kubernetes.core.v1 import Namespace

import config
import infrastructure.builder as infrastructure
import products.products as products
import products.schema_registry as schema_registry
import products.persistor as persistor
import products.schema_registry_validator as schema_registry_validator


def deploy_infrastructure():
    kubernetes_provider = infrastructure.create_cluster(config.cluster)
    broker_resources, brokers_platform_config = infrastructure.create_brokers(config.brokers)
    storage_resources, storage_platform_config = infrastructure.create_storage(config.storage)
    account_platform_config = infrastructure.create_accounts(config.accounts, broker_resources, storage_resources)

    return kubernetes_provider, brokers_platform_config, storage_platform_config, account_platform_config


def create_namespace(namespace_name: str, kubernetes_provider: kubernetes.Provider) -> Namespace:
    return Namespace(
        namespace_name,
        metadata={
            "name": namespace_name
        },
        opts=ResourceOptions(
            provider=kubernetes_provider,
            parent=kubernetes_provider,
        ),
    )


def deploy_products(kubernetes_provider, brokers_platform_config, storage_platform_config, account_platform_config):
    namespace = create_namespace(config.namespace, kubernetes_provider)

    schema_registry_svc_name = None
    if config.deploy_schema_registry:
        schema_registry_values = schema_registry.create_chart_values(config.schema_registry_chart_config, namespace)
        schema_registry_svc_name = schema_registry_values["registrySvcName"]
        products.deploy_chart(schema_registry_values, "dataphos-schema-registry", namespace)

    if config.deploy_persistor:
        persistor_values = persistor.create_chart_values(config.persistor_chart_config, brokers_platform_config, storage_platform_config, account_platform_config, namespace)
        products.deploy_chart(persistor_values, "dataphos-persistor", namespace)

    if config.deploy_schema_registry_validator:
        schema_registry_validator_values = schema_registry_validator.create_chart_values(config.schema_registry_validator_chart_config, schema_registry_svc_name, brokers_platform_config, account_platform_config, namespace)
        products.deploy_chart(schema_registry_validator_values, "dataphos-schema-registry-validator", namespace)


infrastructure_export = deploy_infrastructure()
deploy_products(*infrastructure_export)
