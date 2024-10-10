from pulumi import ComponentResource, ResourceOptions
from pulumi_gcp import organizations

from infrastructure.ResourceCreator import ResourceCreator
import infrastructure.platform.gcp.gcp_config as gcp_config


class GoogleCloudPlatform(ComponentResource, ResourceCreator):

    def __init__(self, retain_projects: str):
        resource_type = 'dataphos:infrastructure:Platform'
        super().__init__(resource_type, "GCP", None, ResourceOptions())

        self._projects = {}
        self.retain_projects = retain_projects

    def get_project(self, project_id: str) -> organizations.Project:
        project = self._projects.get(project_id)
        if project:
            return project

        try:
            project_data = organizations.get_project(project_id)
        except:
            project_data = None

        project_config = { "retain": self.retain_projects }
        opts = ResourceOptions(parent=self)
        project = self.create_or_import_resource(project_id, gcp_config.project_properties, project_config, project_data, opts, self._create_project)
        self._projects[project_id] = project
        self.register_outputs({})
        return project

    def _create_project(self, project_id: str, project_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> organizations.Project:
        return organizations.Project(
            project_id,
            project_id=project_id,
            name=project_config.name or project_id,
            auto_create_network=project_config.auto_create_network,
            billing_account=project_config.billing_account,
            folder_id=project_config.folder_id if project_config.folder_id else None,
            org_id=project_config.org_id if project_config.org_id else None,
            skip_delete=project_config.skip_delete,
            labels=project_config.labels,
            opts=opts
        )
