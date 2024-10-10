import base64

from pulumi import ResourceOptions
from pulumi_azure_native import containerservice, resources
import pulumi_kubernetes as kubernetes

from infrastructure.ResourceCreator import ResourceCreator
from infrastructure.cluster.AbstractKubernetesCluster import AbstractKubernetesCluster
import infrastructure.cluster.aks.aks_config as config


class AksCluster(AbstractKubernetesCluster):

    def __init__(self, cluster_id: str, cluster_config: dict, resource_group: resources.ResourceGroup, parent) -> None:
        self._parent = parent

        self._resource_group_name = resource_group.name
        cluster_name = cluster_config.get("name", cluster_id)
        self._cluster = self._add_cluster(cluster_name, cluster_config)
        self._cluster_name = self._cluster.name if self._cluster else cluster_name

    # interface methods
    def get_kubernetes_provider(self):
        parent = self._cluster if self._cluster else self._parent

        creds = containerservice.list_managed_cluster_user_credentials_output(
            resource_group_name=self._resource_group_name,
            resource_name=self._cluster_name,
        )
        kubeconfig = creds.kubeconfigs[0].value.apply(
            lambda enc: base64.b64decode(enc).decode()
        )
        return kubernetes.Provider(
            "aks-kubernetes-provider",
            kubeconfig=kubeconfig,
            cluster=self._cluster_name,
            opts=ResourceOptions(parent=parent)
        )

    # internal methods
    def _add_cluster(self, cluster_name: str, cluster_config: dict) -> containerservice.ManagedCluster:
        if cluster_config.get("import") is True:
            return None

        cluster_data = None
        opts = ResourceOptions(parent=self._parent)
        return self.create_or_import_resource(cluster_name, config.cluster_properties, cluster_config, cluster_data, opts, self._create_cluster)

    def _create_cluster(self, cluster_name: str, cluster_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> containerservice.ManagedCluster:
        return containerservice.ManagedCluster(
            resource_name=cluster_name,
            resource_name_=cluster_name,
            resource_group_name=self._resource_group_name,
            agent_pool_profiles=[containerservice.ManagedClusterAgentPoolProfileArgs(
                name=pool_profile.get("name"),
                count=pool_profile.get("count"),
                enable_auto_scaling=pool_profile.get("enable_auto_scaling"),
                min_count=pool_profile.get("min_count") if pool_profile.get("enable_auto_scaling") else None,
                max_count=pool_profile.get("max_count") if pool_profile.get("enable_auto_scaling") else None,
                enable_node_public_ip=pool_profile.get("enable_node_public_ip"),
                mode=pool_profile.get("mode"),
                os_disk_size_gb=pool_profile.get("os_disk_size_gb"),
                os_type=pool_profile.get("os_type"),
                type=pool_profile.get("type"),
                vm_size=pool_profile.get("vm_size"),
                tags=pool_profile.get("tags"),
            ) for pool_profile in cluster_config.agent_pool_profiles],
            api_server_access_profile=containerservice.ManagedClusterAPIServerAccessProfileArgs(
                enable_private_cluster=cluster_config.api_server_access_profile["enable_private_cluster"],
            ),
            sku=containerservice.ManagedClusterSKUArgs(
                name=containerservice.ManagedClusterSKUName[cluster_config.sku["name"].upper()],
                tier=containerservice.ManagedClusterSKUTier[cluster_config.sku["tier"].upper()],
            ),
            dns_prefix=cluster_config.dns_prefix or f"{cluster_name}-dns",
            identity=containerservice.ManagedClusterIdentityArgs(
                # Allow only system assigned identity
                type=containerservice.ResourceIdentityType.SYSTEM_ASSIGNED,
            ),
            network_profile=containerservice.ContainerServiceNetworkProfileArgs(
                network_mode=cluster_config.network_profile.get("network_mode"),
                network_plugin=cluster_config.network_profile.get("network_plugin"),
                network_policy=cluster_config.network_profile.get("network_policy"),
                outbound_type=cluster_config.network_profile.get("outbound_type"),
            ),
            tags=cluster_config.tags,
            opts=opts
        )
