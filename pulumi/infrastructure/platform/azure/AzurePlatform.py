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

from pulumi import ComponentResource, ResourceOptions
from pulumi_azure_native import resources

from infrastructure.ResourceCreator import ResourceCreator
import infrastructure.platform.azure.azure_config as azure_config


class AzurePlatform(ComponentResource, ResourceCreator):

    def __init__(self, retain_resource_groups: str, resource_group_tags: dict[str, str]):
        resource_type = 'dataphos:infrastructure:Platform'
        super().__init__(resource_type, "Azure", None, ResourceOptions())

        self._resource_groups = {}
        self.retain_resource_groups = retain_resource_groups
        self.resource_group_tags = resource_group_tags

    def get_resource_group(self, resource_group_name: str) -> resources.ResourceGroup:
        resource_group = self._resource_groups.get(resource_group_name)
        if resource_group:
            return resource_group

        try:
            resource_group_data = resources.get_resource_group(resource_group_name)
        except:
            resource_group_data = None

        resource_group_config = {
            "retain": self.retain_resource_groups,
            "tags": self.resource_group_tags,
        }
        opts = ResourceOptions(parent=self)
        resource_group = self.create_or_import_resource(resource_group_name, azure_config.resource_group_properties, resource_group_config, resource_group_data, opts, self._create_resource_group)
        self._resource_groups[resource_group_name] = resource_group
        self.register_outputs({})
        return resource_group

    def _create_resource_group(self, resource_group_name: str, resource_group_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> resources.ResourceGroup:
        return resources.ResourceGroup(
            resource_group_name,
            resource_group_name=resource_group_name,
            location=resource_group_config.location,
            tags=resource_group_config.tags,
            managed_by=resource_group_config.managed_by,
            opts=opts
        )
