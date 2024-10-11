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


def create_chart_values(schema_registry_values, namespace: Namespace):
    if not schema_registry_values.get("registrySvcName"):
        schema_registry_values["registrySvcName"] = "schema-registry-svc"

    schema_registry_values["namespace"] = namespace._name
    return schema_registry_values
