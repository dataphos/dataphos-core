from typing import Callable, Any

from pulumi import ResourceOptions


class ResourceCreator:
    class ResourceConfigProperties:

        def __init__(self, user_config: dict, resource_data):
            self.user_config = user_config
            self.retrieved_data = resource_data
            self.configuration_updated = False

        # if creating a new resource, resource_data will be empty and default value will be used
        # if importing or updating a resource, default values will be ignored
        def set_property(self, config_key: str, system_default) -> bool:
            variable_name = ResourceCreator.camel_case_to_snake_case(config_key)

            default_value = getattr(self.retrieved_data, variable_name) if self.retrieved_data else system_default
            value = self.user_config.get(config_key, default_value)
            setattr(self, variable_name, value)
            return self.retrieved_data is not None and value != default_value

        def set_dict_property(self, config_key: str, system_default: dict) -> bool:
            variable_name = ResourceCreator.camel_case_to_snake_case(config_key)
            retrieved_dict = getattr(self.retrieved_data, variable_name) if self.retrieved_data else None
            user_dict = self.user_config.get(config_key, {})

            if self.retrieved_data and not retrieved_dict and not user_dict:
                setattr(self, variable_name, retrieved_dict)
                return False

            setattr(self, variable_name, {})
            value_changed = False
            for nested_key in system_default:
                key_name = ResourceCreator.camel_case_to_snake_case(nested_key)
                retrieved_value = retrieved_dict.get(key_name) if retrieved_dict else None
                default_value = retrieved_value if self.retrieved_data else system_default[nested_key]

                value = user_dict.get(nested_key, default_value)
                getattr(self, variable_name)[key_name] = value

                if not value_changed:
                    value_changed = value != default_value
            return self.retrieved_data is not None and value_changed

        def set_list_property(self, config_key: str, system_default: list[dict]) -> bool:
            variable_name = ResourceCreator.camel_case_to_snake_case(config_key)
            retrieved_list = getattr(self.retrieved_data, variable_name) if self.retrieved_data else None
            user_list = self.user_config.get(config_key, [{}])

            if self.retrieved_data and not retrieved_list and not user_list:
                setattr(self, variable_name, retrieved_list)
                return False

            value_changed = False
            # special case of a single-element dictionary list
            if not (user_list and len(user_list) > 1) and not (retrieved_list and len(retrieved_list) > 1) and len(system_default) == 1:
                setattr(self, variable_name, [{}])
                for nested_key in system_default[0]:
                    key_name = ResourceCreator.camel_case_to_snake_case(nested_key)
                    retrieved_value = retrieved_list[0].get(key_name) if retrieved_list else None
                    default_value = retrieved_value if self.retrieved_data else system_default[0][nested_key]

                    value = user_list[0].get(nested_key, default_value)
                    getattr(self, variable_name)[0][key_name] = value

                    if not value_changed:
                        value_changed = value != default_value
            else:
                if config_key in self.user_config:
                    self.user_config[config_key] = ResourceCreator.dict_list_to_snake_case(user_list)
                system_default = ResourceCreator.dict_list_to_snake_case(system_default)
                value_changed = self.set_property(config_key, system_default)
            return self.retrieved_data is not None and value_changed

    @staticmethod
    def camel_case_to_snake_case(s: str) -> str:
        return ''.join(['_'+i.lower() if i.isupper() else i for i in s]).lstrip('_')

    @staticmethod
    def dict_list_to_snake_case(original: list[dict]) -> list[dict]:
        new = []
        for config_map in original:
            d = {}
            for key, value in config_map.items():
                new_key = ResourceCreator.camel_case_to_snake_case(key)
                d[new_key] = value
            new.append(d)
        return new

    def _configure_resource(self, config_properties: dict, user_config: dict, retrieved_data):
        resource_config = ResourceCreator.ResourceConfigProperties(user_config, retrieved_data)
        for config_key, config_value in config_properties.items():
            if type(config_value) is dict:
                value_updated = resource_config.set_dict_property(config_key, system_default=config_value)
            elif type(config_value) is list and type(config_value[0]) is dict:
                value_updated = resource_config.set_list_property(config_key, system_default=config_value)
            else:
                value_updated = resource_config.set_property(config_key, system_default=config_value)

            if not resource_config.configuration_updated and value_updated:
                resource_config.configuration_updated = True
        return resource_config

    def create_or_import_resource(self, resource_name: str, resource_properties: dict, user_config: dict, retrieved_data, opts: ResourceOptions, create_resource: Callable[[str,  ResourceConfigProperties, ResourceOptions], Any]):
        # Cannot import existing resource and update its configuration in one run
        # Import the resource first, then run the script again with desired configuration
        resource_config = self._configure_resource(resource_properties, user_config, retrieved_data)
        opts.retain_on_delete = user_config.get("retain", False) is True

        if retrieved_data:
            # Resource already exists
            if resource_config.configuration_updated:
                # If any additional values are configured, try to update properties with configured values
                # resource must had been imported before it can be updated
                # otherwise it will try creating it and deployment will fail
                print(f"Updating existing resource <{resource_name}> configuration")
            else:
                # Import existing resource
                opts.import_ = retrieved_data.id
                print(f"Imported existing resource <{resource_name}>")
        else:
            # Create a new resource using configured values
            print(f"Creating new resource <{resource_name}>")

        return create_resource(resource_name, resource_config, opts)
