from pulumi import ComponentResource, ResourceOptions

from infrastructure.platform.Platform import Platform
from infrastructure.broker.AbstractMessageBroker import AbstractMessageBroker
from infrastructure.broker.service_bus.ServiceBusMessageBroker import ServiceBusMessageBroker
from infrastructure.broker.pubsub.PubSubMessageBroker import PubSubMessageBroker
from infrastructure.broker.kafka.KafkaMessageBroker import KafkaMessageBroker


class MessageBroker(ComponentResource, AbstractMessageBroker):

    def __init__(self, broker_id: str, broker_config: dict, platform: Platform) -> None:
        resource_type = "dataphos:infrastructure:MessageBroker"
        resource_name = f"{broker_id}-broker"
        workspace = platform.get_workspace(broker_config)
        opts = ResourceOptions(parent=workspace)
        super().__init__(resource_type, resource_name, None, opts)

        broker_type = broker_config["type"]
        if broker_type == "servicebus":
            self._broker_instance = ServiceBusMessageBroker(broker_id, broker_config, resource_group=workspace, parent=self)
        elif broker_type == "pubsub":
            self._broker_instance = PubSubMessageBroker(broker_id, broker_config, project=workspace, parent=self)
        elif broker_type == "kafka":
            self._broker_instance = KafkaMessageBroker(broker_id, broker_config, kubernetes_provider=workspace, parent=self)

    def add_topic(self, topic_name: str, topic_config: dict):
        return self._broker_instance.add_topic(topic_name, topic_config)

    def add_subscription(self, topic_name: str, subscription_name: str, subscription_config: dict):
        return self._broker_instance.add_subscription(topic_name, subscription_name, subscription_config)

    def export_config(self) -> dict:
        return self._broker_instance.export_config()

    def get_instance(self) -> AbstractMessageBroker:
        return self._broker_instance
