from pulumi import ResourceOptions
from pulumi_azure_native import servicebus, resources

from infrastructure.ResourceCreator import ResourceCreator
from infrastructure.broker.AbstractMessageBroker import AbstractMessageBroker
import infrastructure.broker.service_bus.servicebus_config as config


class ServiceBusMessageBroker(AbstractMessageBroker):

    def __init__(self, broker_id: str, broker_config: dict, resource_group: resources.ResourceGroup, parent) -> None:
        self._parent = parent
        self._resource_group_name = resource_group.name

        self.namespace_name = broker_config.get("azsbNamespace", broker_id)
        self.namespace = self._add_namespace(self.namespace_name, broker_config)
        self._connection_string = self._get_connection_string()

        self.topics = {}
        self.subscriptions = {}

    # interface methods
    def add_topic(self, topic_name: str, topic_config: dict):
        topic_data = self._get_topic(topic_name)

        opts = ResourceOptions(parent=self.namespace)
        topic = self.create_or_import_resource(topic_name, config.topic_properties, topic_config, topic_data, opts, self._create_topic)
        self.topics[topic_name] = topic
        self.subscriptions[topic_name] = {}
        return topic

    def add_subscription(self, topic_name: str, subscription_name: str, subscription_config: dict):
        subscription_data = self._get_subscription(topic_name, subscription_name)

        topic = self.topics[topic_name]
        opts = ResourceOptions(parent=topic)
        subscription = self.create_or_import_resource(subscription_name, config.subscription_properties, subscription_config, subscription_data, opts, self._create_subscription)
        self.subscriptions[topic_name][subscription_name] = subscription
        return subscription

    def export_config(self) -> dict:
        platform_config = {
            "connectionString": self._connection_string,
        }
        return platform_config

    # internal methods
    def _add_namespace(self, namespace_name: str, broker_config: dict) -> servicebus.Namespace:
        namespace_data = self._get_namespace(namespace_name)
        opts = ResourceOptions(parent=self._parent)
        return self.create_or_import_resource(namespace_name, config.namespace_properties, broker_config, namespace_data, opts, self._create_namespace)

    def _get_namespace(self, namespace_name: str) -> servicebus.Namespace:
        try:
            namespace_data = servicebus.get_namespace(
                namespace_name=namespace_name,
                resource_group_name=self._resource_group_name
            )
        except:
            namespace_data = None
        return namespace_data

    def _create_namespace(self, namespace_name: str, namespace_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> servicebus.Namespace:
        return servicebus.Namespace(
            namespace_name,
            namespace_name=namespace_name,
            resource_group_name=self._resource_group_name,
            location=namespace_config.location,
            sku=servicebus.SBSkuArgs(
                name=servicebus.SkuName[namespace_config.sku["name"].upper()],
                tier=servicebus.SkuTier[namespace_config.sku["tier"].upper()],
                capacity=namespace_config.sku.get("capacity"),
            ),
            disable_local_auth=namespace_config.disable_local_auth,
            minimum_tls_version=namespace_config.minimum_tls_version,
            zone_redundant=namespace_config.zone_redundant,
            tags=namespace_config.tags,
            opts=opts
        )

    def _get_connection_string(self):
        keys = servicebus.list_namespace_keys_output(
            authorization_rule_name="RootManageSharedAccessKey",
            resource_group_name=self._resource_group_name,
            namespace_name=self.namespace.name,
        )
        return keys.primary_connection_string

    def _get_topic(self, topic_name: str) -> servicebus.Topic:
        try:
            topic_data = servicebus.get_topic(
                namespace_name=self.namespace.name,
                resource_group_name=self._resource_group_name,
                topic_name=topic_name
            )
        except:
            topic_data = None
        return topic_data

    def _create_topic(self, topic_name: str, topic_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> servicebus.Topic:
        return servicebus.Topic(
            topic_name,
            topic_name=topic_name,
            resource_group_name=self._resource_group_name,
            namespace_name=self.namespace.name,
            auto_delete_on_idle=topic_config.auto_delete_on_idle,
            default_message_time_to_live=topic_config.default_message_time_to_live,
            duplicate_detection_history_time_window=topic_config.duplicate_detection_history_time_window,
            enable_batched_operations=topic_config.enable_batched_operations,
            enable_express=topic_config.enable_express,
            enable_partitioning=topic_config.enable_partitioning,
            max_size_in_megabytes=topic_config.max_size_in_megabytes,
            requires_duplicate_detection=topic_config.requires_duplicate_detection,
            status=topic_config.status,
            support_ordering=topic_config.support_ordering,
            max_message_size_in_kilobytes=topic_config.max_message_size_in_kilobytes,
            opts=opts
        )

    def _get_subscription(self, topic_name: str, subscription_name: str) -> servicebus.Subscription:
        try:
            subscription_data = servicebus.get_subscription(
                namespace_name=self.namespace.name,
                resource_group_name=self._resource_group_name,
                topic_name=topic_name,
                subscription_name=subscription_name
            )
        except:
            subscription_data = None
        return subscription_data

    def _create_subscription(self, subscription_name: str, subscription_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> servicebus.Subscription:
        topic_name = opts.parent._name
        return servicebus.Subscription(
            f"{topic_name}-{subscription_name}",
            topic_name=topic_name,
            subscription_name=subscription_name,
            namespace_name=self.namespace.name,
            resource_group_name=self._resource_group_name,
            max_delivery_count=subscription_config.max_delivery_count,
            lock_duration=subscription_config.lock_duration,
            auto_delete_on_idle=subscription_config.auto_delete_on_idle,
            dead_lettering_on_filter_evaluation_exceptions=subscription_config.dead_lettering_on_filter_evaluation_exceptions,
            dead_lettering_on_message_expiration=subscription_config.dead_lettering_on_message_expiration,
            default_message_time_to_live=subscription_config.default_message_time_to_live,
            duplicate_detection_history_time_window=subscription_config.duplicate_detection_history_time_window,
            enable_batched_operations=subscription_config.enable_batched_operations,
            forward_to=subscription_config.forward_to,
            forward_dead_lettered_messages_to=subscription_config.forward_dead_lettered_messages_to,
            requires_session=subscription_config.requires_session,
            status=subscription_config.status,
            is_client_affine=subscription_config.is_client_affine,
            opts=opts
        )
