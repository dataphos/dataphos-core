from pulumi_kubernetes.core.v1 import Namespace


def create_chart_values(schema_registry_values, namespace: Namespace):
    if not schema_registry_values.get("registrySvcName"):
        schema_registry_values["registrySvcName"] = "schema-registry-svc"

    schema_registry_values["namespace"] = namespace._name
    return schema_registry_values
