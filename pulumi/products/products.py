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
