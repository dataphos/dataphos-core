from pulumi_kubernetes.core.v1 import Namespace

import products.products as products


def create_chart_values(schema_registry_validator_values, schema_registry_svc_name, brokers_platform_config, account_platform_config, namespace: Namespace):
    if not schema_registry_validator_values.get("schemaRegistryURL") and schema_registry_svc_name:
        schema_registry_validator_values["schemaRegistryURL"] = f"http://{schema_registry_svc_name}:8080"

    schema_registry_validator_values = products.update_values(schema_registry_validator_values, brokers_platform_config, "brokers")
    schema_registry_validator_values = products.update_values(schema_registry_validator_values, account_platform_config, "validator")

    schema_registry_validator_values["namespace"] = namespace._name
    return schema_registry_validator_values
