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
