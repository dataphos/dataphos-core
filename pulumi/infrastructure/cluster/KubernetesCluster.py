from pulumi import ComponentResource, ResourceOptions

from infrastructure.platform.Platform import Platform
from infrastructure.cluster.AbstractKubernetesCluster import AbstractKubernetesCluster
from infrastructure.cluster.aks.AksCluster import AksCluster
from infrastructure.cluster.gke.GkeCluster import GkeCluster


class KubernetesCluster(ComponentResource, AbstractKubernetesCluster):

    def __init__(self, cluster_id: str, cluster_config: dict, platform: Platform) -> None:
        resource_type = "dataphos:infrastructure:KubernetesCluster"
        resource_name = f"{cluster_id}-cluster"
        workspace = platform.get_workspace(cluster_config)
        opts = ResourceOptions(parent=workspace)
        super().__init__(resource_type, resource_name, None, opts)

        cluster_type = cluster_config["type"]
        if cluster_type == "aks":
            self._cluster_instance = AksCluster(cluster_id, cluster_config, resource_group=workspace, parent=self)
        elif cluster_type == "gke":
            self._cluster_instance = GkeCluster(cluster_id, cluster_config, project=workspace, parent=self)

        self.register_outputs({})

    def get_kubernetes_provider(self):
        return self._cluster_instance.get_kubernetes_provider()
