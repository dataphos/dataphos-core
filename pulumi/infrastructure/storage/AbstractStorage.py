from abc import ABC, abstractmethod

from infrastructure.ResourceCreator import ResourceCreator


class AbstractStorage(ABC, ResourceCreator):

    @abstractmethod
    def add_bucket(self, bucket_name: str, bucket_config: dict):
        raise NotImplementedError

    @abstractmethod
    def export_config(self) -> dict:
        raise NotImplementedError
