from pulumi import ResourceOptions
from pulumi_gcp import organizations, storage

from infrastructure.ResourceCreator import ResourceCreator
from infrastructure.storage.AbstractStorage import AbstractStorage
import infrastructure.storage.gcs.gcs_config as gcs_config
from config import resource_tags


class GoogleCloudStorage(AbstractStorage):

    def __init__(self, storage_id: str, storage_config: dict, project: organizations.Project, parent) -> None:
        self._parent = parent
        self._project_id = project.project_id

        self.project_id = storage_config["projectID"]
        self.buckets = {}

    # interface methods
    def add_bucket(self, bucket_name: str, bucket_config: dict):
        bucket_data = self._get_bucket(bucket_name)

        if resource_tags and not bucket_config.get("labels"):
            bucket_config["labels"] = resource_tags

        opts = ResourceOptions(parent=self._parent)
        bucket = self.create_or_import_resource(bucket_name, gcs_config.bucket_config, bucket_config, bucket_data, opts, self._create_bucket)
        self.buckets[bucket_name] = bucket
        return bucket

    def export_config(self) -> dict:
        platform_config = {
            "projectID": self.project_id,
        }
        return platform_config

    # internal methods
    def _get_bucket(self, bucket_name: str) -> storage.Bucket:
        try:
            bucket_data = storage.get_bucket(
                name=bucket_name
            )
        except:
            bucket_data = None
        return bucket_data

    def _create_bucket(self, bucket_name: str, bucket_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> storage.Bucket:
        return storage.Bucket(
            resource_name=bucket_name,
            name=bucket_name,
            project=self._project_id,
            location=bucket_config.location,
            public_access_prevention=bucket_config.public_access_prevention,
            uniform_bucket_level_access=bucket_config.uniform_bucket_level_access,
            labels=bucket_config.labels,
            opts=opts
        )
