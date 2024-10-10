from pulumi import ComponentResource, ResourceOptions

from infrastructure.platform.Platform import Platform
from infrastructure.storage.AbstractStorage import AbstractStorage
from infrastructure.storage.abs.AzureBlobStorage import AzureBlobStorage
from infrastructure.storage.gcs.GoogleCloudStorage import GoogleCloudStorage


class Storage(ComponentResource, AbstractStorage):

    def __init__(self, storage_id: str, storage_config: dict, platform: Platform) -> None:
        resource_type = 'dataphos:infrastructure:Storage'
        resource_name = f"{storage_id}-storage"
        workspace = platform.get_workspace(storage_config)
        opts = ResourceOptions(parent=workspace)
        super().__init__(resource_type, resource_name, None, opts)

        storage_type = storage_config["type"]
        if storage_type == "abs":
            self._storage_instance = AzureBlobStorage(storage_id, storage_config, resource_group=workspace, parent=self)
        elif storage_type == "gcs":
            self._storage_instance = GoogleCloudStorage(storage_id, storage_config, project=workspace, parent=self)

    def add_bucket(self, bucket_name: str, bucket_config: dict):
        return self._storage_instance.add_bucket(bucket_name, bucket_config)

    def export_config(self) -> dict:
        return self._storage_instance.export_config()

    def get_instance(self) -> AbstractStorage:
        return self._storage_instance
