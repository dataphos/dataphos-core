from pulumi import ResourceOptions, Output
from pulumi.resource import CustomTimeouts
from pulumi_kubernetes import Provider
from pulumi_kubernetes.helm.v3 import Chart, LocalChartOpts
from pulumi_kubernetes.core.v1 import Namespace, ServicePatch, ServiceSpecPatchArgs, ServicePortPatchArgs
from pulumi_kubernetes.meta.v1 import ObjectMetaPatchArgs
from pulumi_kubernetes.yaml import ConfigFile

from infrastructure.ResourceCreator import ResourceCreator
from infrastructure.broker.AbstractMessageBroker import AbstractMessageBroker
import infrastructure.broker.kafka.kafka_config as config


class KafkaMessageBroker(AbstractMessageBroker):

    def __init__(self, broker_id: str, broker_config: dict, kubernetes_provider: Provider, parent) -> None:
        self._parent = parent

        strimzi_operator_namespace = broker_config.get("strimziOperatorNamespace", config.cluster_properties["strimziOperatorNamespace"])
        self._kafka_cluster_namespace = broker_config.get("clusterNamespace", config.cluster_properties["clusterNamespace"])
        self._kafka_cluster_name = broker_config.get("clusterName", config.cluster_properties["clusterName"])

        self._kafka_cluster = None
        self._broker_addr = broker_config.get("bootstrapServers")
        if self._broker_addr: return

        strimzi_ns = self._create_namespace(strimzi_operator_namespace, kubernetes_provider)
        kafka_ns = self._create_namespace(self._kafka_cluster_namespace, kubernetes_provider)
        strimzi_operator = self._deploy_strimzi_cluster_operator(strimzi_ns, kafka_ns)
        self._kafka_cluster = self._add_kafka_cluster(self._kafka_cluster_name, broker_config, strimzi_operator, kafka_ns)
        self._broker_addr = self._get_broker_addr(self._kafka_cluster)

    # interface methods
    def add_topic(self, topic_name: str, topic_config: dict):
        topic_data = None
        opts = ResourceOptions(parent=self._kafka_cluster, depends_on=self._kafka_cluster)
        return self.create_or_import_resource(topic_name, config.topic_properties, topic_config, topic_data, opts, self._create_topic)

    def add_subscription(self, topic_name: str, subscription_name: str, subscription_config: dict):
        return None

    def export_config(self) -> dict:
        kafka_config = {
            "brokerAddr": self._broker_addr,
        }
        return kafka_config

    # internal methods
    def _deploy_strimzi_cluster_operator(self, strimzi_ns: Namespace, kafka_ns: Namespace):
        values = {
            "watchNamespaces": [kafka_ns._name]
        }

        return Chart(
            release_name="strimzi-kafka-operator",
            config=LocalChartOpts(
                path=f"../helm_charts/strimzi-kafka-operator",
                namespace=strimzi_ns._name,
                values=values,
            ),
            opts=ResourceOptions(
                parent=strimzi_ns,
            )
        )

    def _add_kafka_cluster(self, cluster_name: str, cluster_config: dict, strimzi_operator: Chart, kafka_ns: Namespace):
        cluster_data = None
        opts = ResourceOptions(parent=kafka_ns, depends_on=strimzi_operator.ready)
        return self.create_or_import_resource(cluster_name, config.cluster_properties, cluster_config, cluster_data, opts, self._create_kafka)

    def _create_namespace(self, namespace_name: str, kubernetes_provider: Provider) -> Namespace:
        return Namespace(
            namespace_name,
            metadata={
                "name": namespace_name
            },
            opts=ResourceOptions(
                provider=kubernetes_provider,
                parent=self._parent,
            ),
        )

    def _create_kafka(self, kafka_name: str, kafka_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> ConfigFile:
        def configure_kafka(obj, opts):
            obj["metadata"]["namespace"] = self._kafka_cluster_namespace
            if obj["kind"] != "Kafka": return
            obj["metadata"]["name"] = kafka_name
            obj["spec"]["kafka"]["listeners"] = kafka_config.listeners

        return ConfigFile(kafka_name,
            file="./infrastructure/broker/kafka/resources/kafka-metrics.yaml",
            transformations=[configure_kafka],
            opts=opts)

    def _get_broker_addr(self, kafka_cluster: ConfigFile):
        bootstrap_svc_name = f"{self._kafka_cluster_name}-kafka-bootstrap"
        internal_ports = [ServicePortPatchArgs(port=9091, name="tcp-replication")]
        internal_ports.extend(
            [ServicePortPatchArgs(port=l['port'], name=f"tcp-{l['name']}") for l in config.cluster_properties["listeners"] if l['type'] == "internal"]
        )

        bootstrap_svc = ServicePatch(bootstrap_svc_name,
            metadata=ObjectMetaPatchArgs(
                name=bootstrap_svc_name,
                namespace=self._kafka_cluster_namespace,
            ),
            spec=ServiceSpecPatchArgs(ports=internal_ports),
            opts=ResourceOptions(
                parent=kafka_cluster,
                depends_on=kafka_cluster,
                custom_timeouts=CustomTimeouts(create='20m')
            )
        )

        return bootstrap_svc.spec.apply(lambda spec:
            Output.format(",".join([f"{spec.get('cluster_ip')}:{port['port']}" for port in spec['ports'][1:]])))

    def _create_topic(self, topic_name: str, topic_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> ConfigFile:
        def set_config_param(obj, key, param):
            if not param: return
            if not obj["spec"].get("config"):
                obj["spec"]["config"] = {}
            obj["spec"]["config"][key] = param

        def configure_topic(obj, opts):
            obj["metadata"]["name"] = topic_name
            obj["metadata"]["namespace"] = self._kafka_cluster_namespace
            obj["metadata"]["labels"]["strimzi.io/cluster"] = self._kafka_cluster_name
            obj["spec"]["partitions"] = topic_config.partitions
            obj["spec"]["replicas"] = topic_config.replicas
            set_config_param(obj, "retention.ms", topic_config.config["retention_ms"])
            set_config_param(obj, "segment.bytes", topic_config.config["segment_bytes"])

        return ConfigFile(topic_name,
            file="./infrastructure/broker/kafka/resources/kafka-topic.yaml",
            transformations=[configure_topic],
            opts=opts)
