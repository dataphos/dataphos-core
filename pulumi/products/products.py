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
from pulumi_kubernetes.helm.v3 import Chart, LocalChartOpts
from pulumi_kubernetes.core.v1 import Namespace


def update_values(values, config, component_name):
    for instance_id in values.get(component_name, {}):
        instance_config = config.get(instance_id, {})
        values[component_name][instance_id].update(instance_config)
    return values


def deploy_chart(values, name, namespace: Namespace):
    Chart(
        release_name=name,
        config=LocalChartOpts(
            path="../helm_charts/" + name,
            values=values,
        ),
        opts=ResourceOptions(
            parent=namespace
        )
    )
