from abc import ABC, abstractmethod

from infrastructure.broker.AbstractMessageBroker import AbstractMessageBroker
from infrastructure.storage.AbstractStorage import AbstractStorage


class AbstractAccount(ABC):

    @abstractmethod
    def add_broker_role(self, broker: AbstractMessageBroker, role_config: dict):
        raise NotImplementedError

    @abstractmethod
    def add_storage_role(self, storage: AbstractStorage, role_config: dict):
        raise NotImplementedError

    @abstractmethod
    def export_config(self):
        raise NotImplementedError
