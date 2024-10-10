from abc import ABC, abstractmethod

from infrastructure.ResourceCreator import ResourceCreator


class AbstractMessageBroker(ABC, ResourceCreator):

    @abstractmethod
    def add_topic(self, topic_name: str, topic_config: dict):
        raise NotImplementedError

    @abstractmethod
    def add_subscription(self, topic_name: str, subscription_name: str, subscription_config: dict):
        raise NotImplementedError

    @abstractmethod
    def export_config(self) -> dict:
        raise NotImplementedError
