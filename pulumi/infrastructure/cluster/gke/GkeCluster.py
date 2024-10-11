# Copyright 2024 Syntio Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pulumi import ResourceOptions, Output
from pulumi_gcp import container, organizations
import pulumi_kubernetes as kubernetes

from infrastructure.ResourceCreator import ResourceCreator
from infrastructure.cluster.AbstractKubernetesCluster import AbstractKubernetesCluster
import infrastructure.cluster.gke.gke_config as gke_config
from config import resource_tags


class GkeCluster(AbstractKubernetesCluster):

    def __init__(self, cluster_id: str, cluster_config: dict, project: organizations.Project, parent) -> None:
        self._parent = parent
        self._project_id = project.project_id
        cluster_name = cluster_config.get("name", cluster_id)
        self._cluster = self._add_cluster(cluster_name, cluster_config)

    # interface methods
    def get_kubernetes_provider(self):
        # Manufacture a GKE-style Kubeconfig. Note that this is slightly "different" because of the way GKE requires
        # gcloud to be in the picture for cluster authentication (rather than using the client cert/key directly).
        kubernetes_info = Output.all(self._cluster.name, self._cluster.endpoint, self._cluster.master_auth)
        kubeconfig = Output.all(info=kubernetes_info, project_id=self._project_id, location=self._cluster.location).apply(
            lambda args: gke_config.kubeconfig_template.format(
                args['info'][2]['cluster_ca_certificate'], args['info'][1], '{0}_{1}_{2}'.format(
                    args['project_id'], args['location'], args['info'][0]
                )
            )
        )
        return kubernetes.Provider(
            "gke-kubernetes-provider",
            kubeconfig=kubeconfig,
            opts=ResourceOptions(parent=self._cluster)
        )

    # internal methods
    def _add_cluster(self, cluster_name: str, cluster_config: dict) -> container.Cluster:
        cluster_data = self._get_cluster(cluster_name, cluster_config.get("location"))

        if resource_tags and not cluster_config.get("resourceLabels"):
            cluster_config["resourceLabels"] = resource_tags

        opts = ResourceOptions(parent=self._parent)
        return self.create_or_import_resource(cluster_name, gke_config.cluster_properties, cluster_config, cluster_data, opts, self._create_cluster)

    def _get_cluster(self, cluster_name: str, location: str) -> container.AwaitableGetClusterResult:
        try:
            cluster_data = container.get_cluster(
                name=cluster_name,
                project=self._project_id,
                location=location,
            )
        except:
            cluster_data = None
        return cluster_data

    def _create_cluster(self, cluster_name: str, cluster_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> container.Cluster:
        return container.Cluster(
            cluster_name,
            name=cluster_name,
            project=self._project_id,
            initial_node_count=cluster_config.initial_node_count,
            node_config=container.ClusterNodeConfigArgs(
                machine_type=cluster_config.node_configs[0]["machine_type"],
                oauth_scopes=cluster_config.node_configs[0]["oauth_scopes"],
            ),
            cluster_autoscaling=container.ClusterClusterAutoscalingArgs(
                autoscaling_profile=cluster_config.cluster_autoscalings[0]["autoscaling_profile"],
                enabled=cluster_config.cluster_autoscalings[0]["enabled"],
                resource_limits=cluster_config.cluster_autoscalings[0]["resource_limits"],
            ) if cluster_config.cluster_autoscalings and cluster_config.cluster_autoscalings[0]["enabled"] else None,
            enable_shielded_nodes=cluster_config.enable_shielded_nodes,
            binary_authorization=container.ClusterBinaryAuthorizationArgs(
                evaluation_mode=cluster_config.binary_authorizations[0]["evaluation_mode"],
            ) if cluster_config.binary_authorizations and cluster_config.binary_authorizations[0]["evaluation_mode"] else None,
            vertical_pod_autoscaling=container.ClusterVerticalPodAutoscalingArgs(
                enabled=cluster_config.vertical_pod_autoscalings[0]["enabled"],
            ) if cluster_config.vertical_pod_autoscalings and cluster_config.vertical_pod_autoscalings[0]["enabled"] is not None else None,
            resource_labels=cluster_config.resource_labels,
            opts=opts
        )
