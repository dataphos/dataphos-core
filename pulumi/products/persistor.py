from pulumi_kubernetes.core.v1 import Namespace

import products.products as products


def create_chart_values(persistor_values, brokers_platform_config, storage_platform_config, account_platform_config, namespace: Namespace):
    persistor_values = products.update_values(persistor_values, brokers_platform_config, "brokers")
    persistor_values = products.update_values(persistor_values, storage_platform_config, "storage")

    product_names = ["persistor", "indexer", "resubmitter"]
    for name in product_names:
        persistor_values = products.update_values(persistor_values, account_platform_config, name)

    persistor_values["namespace"] = namespace._name

    return persistor_values
