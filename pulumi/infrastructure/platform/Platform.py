import pulumi_kubernetes as kubernetes

from infrastructure.platform.azure.AzurePlatform import AzurePlatform
from infrastructure.platform.gcp.GoogleCloudPlatform import GoogleCloudPlatform
from infrastructure.platform.PlatformID import PlatformID
import config


class Platform():
    RESOURCE_TYPE_TO_PLATFORM_MAP = {
        "abs": PlatformID.AZURE,
        "aks": PlatformID.AZURE,
        "servicebus": PlatformID.AZURE,
        "gcs": PlatformID.GCP,
        "gke": PlatformID.GCP,
        "pubsub": PlatformID.GCP,
        "kafka": PlatformID.NONE,
    }

    PLATFORM_ID_TO_WORKSPACE_KEY_MAP = {
        PlatformID.AZURE: "resourceGroup",
        PlatformID.GCP: "projectID",
        PlatformID.NONE: None,
    }

    def __init__(self):
        self._azure_platform: AzurePlatform = None
        self._gcp_platform: GoogleCloudPlatform = None

    @staticmethod
    def get_platform(resource_type: str) -> PlatformID:
        return Platform.RESOURCE_TYPE_TO_PLATFORM_MAP[resource_type]

    @staticmethod
    def get_workspace_key(platform_id: PlatformID) -> str:
        return Platform.PLATFORM_ID_TO_WORKSPACE_KEY_MAP[platform_id]

    def set_kubernetes_provider(self, kubernetes_provider: kubernetes.Provider) -> None:
        self._kubernetes_provider = kubernetes_provider

    def get_workspace(self, resource_config: dict):
        platform = resource_config.get("platform") or Platform.get_platform(resource_config["type"])
        if platform == PlatformID.AZURE:
            if self._azure_platform is None:
                self._azure_platform = AzurePlatform(config.retain_resource_groups, config.resource_tags)
            return self._azure_platform.get_resource_group(resource_group_name=resource_config["resourceGroup"])
        elif platform == PlatformID.GCP:
            if self._gcp_platform is None:
                self._gcp_platform = GoogleCloudPlatform(config.retain_projects)
            return self._gcp_platform.get_project(project_id=resource_config["projectID"])
        else:
            # Resources without a configured platform are considered Kubernetes resources
            return self._kubernetes_provider
