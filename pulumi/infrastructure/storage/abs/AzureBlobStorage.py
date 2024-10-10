from pulumi import ResourceOptions
from pulumi_azure_native import storage, resources

from infrastructure.ResourceCreator import ResourceCreator
from infrastructure.storage.AbstractStorage import AbstractStorage
import infrastructure.storage.abs.abs_config as config


class AzureBlobStorage(AbstractStorage):

    def __init__(self, storage_id: str, storage_config: dict, resource_group: resources.ResourceGroup, parent) -> None:
        self._parent = parent
        self._resource_group_name = resource_group.name

        self.account_name = storage_config.get("accountStorageID", storage_id)
        self.storage_account = self._add_storage_account(self.account_name, storage_config)

        self.containers = {}

    # interface methods
    def add_bucket(self, bucket_name: str, bucket_config: dict):
        bucket_data = self._get_blob_container(bucket_name)

        opts = ResourceOptions(parent=self.storage_account)
        bucket = self.create_or_import_resource(bucket_name, config.container_properties, bucket_config, bucket_data, opts, self._create_blob_container)
        self.containers[bucket_name] = bucket
        return bucket

    def export_config(self) -> dict:
        platform_config = {
            "accountStorageID": self.account_name,
        }
        return platform_config

    # internal methods
    def _add_storage_account(self, account_name: str, storage_config: dict) -> storage.StorageAccount:
        account_data = self._get_storage_account(account_name)
        opts = ResourceOptions(parent=self._parent)
        return self.create_or_import_resource(account_name, config.account_properties, storage_config, account_data, opts, self._create_storage_account)

    def _get_storage_account(self, account_name: str) -> storage.StorageAccount:
        try:
            account_data = storage.get_storage_account(
                account_name=account_name,
                resource_group_name=self._resource_group_name
            )
        except:
            account_data = None
        return account_data

    def _create_storage_account(self, account_name: str, account_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> storage.StorageAccount:
        return storage.StorageAccount(
            account_name,
            account_name=account_name,
            resource_group_name=self._resource_group_name,
            kind=account_config.kind,
            allow_blob_public_access=account_config.allow_blob_public_access,
            allow_cross_tenant_replication=account_config.allow_cross_tenant_replication,
            allow_shared_key_access=account_config.allow_shared_key_access,
            default_to_o_auth_authentication=account_config.default_to_o_auth_authentication,
            dns_endpoint_type=account_config.dns_endpoint_type,
            enable_https_traffic_only=account_config.enable_https_traffic_only,
            enable_nfs_v3=account_config.enable_nfs_v3,
            is_hns_enabled=account_config.is_hns_enabled,
            minimum_tls_version=storage.MinimumTlsVersion[account_config.minimum_tls_version],
            public_network_access=account_config.public_network_access,
            large_file_shares_state=account_config.large_file_shares_state,
            access_tier=storage.AccessTier[account_config.access_tier.upper()] if account_config.access_tier else None,
            sku=storage.SkuArgs(
                name=storage.SkuName[account_config.sku["name"].upper()],
            ),
            encryption=storage.EncryptionArgs(
                key_source=account_config.encryption.get("key_source"),
                require_infrastructure_encryption=account_config.encryption.get("require_infrastructure_encryption", None),
                encryption_identity=None,
                key_vault_properties=None,
                services=storage.EncryptionServicesArgs(
                    blob=storage.EncryptionServiceArgs(
                        enabled=account_config.encryption["services"]["blob"].get("enabled"),
                        key_type=account_config.encryption["services"]["blob"].get("key_type")
                    ),
                    file=storage.EncryptionServiceArgs(
                        enabled=account_config.encryption["services"]["file"].get("enabled"),
                        key_type=account_config.encryption["services"]["file"].get("key_type")
                    ),
                    queue=None,
                    table=None,
                )
            ),
            network_rule_set=storage.NetworkRuleSetArgs(
                default_action=account_config.network_rule_set.get("default_action"),
                bypass=account_config.network_rule_set.get("bypass"),
                ip_rules=None,
                resource_access_rules=None,
                virtual_network_rules=None
            ),
            azure_files_identity_based_authentication=None,
            custom_domain=None,
            identity=None,
            key_policy=None,
            routing_preference=None,
            sas_policy=None,
            location=account_config.location,
            extended_location=None,
            tags=account_config.tags,
            opts=opts
        )

    def _get_blob_container(self, container_name: str) -> storage.BlobContainer:
        try:
            container_data = storage.get_blob_container(
                account_name=self.account_name,
                resource_group_name=self._resource_group_name,
                container_name=container_name
            )
        except:
            container_data = None
        return container_data

    def _create_blob_container(self, container_name: str, container_config: ResourceCreator.ResourceConfigProperties, opts: ResourceOptions) -> storage.BlobContainer:
        return storage.BlobContainer(
            container_name,
            container_name=container_name,
            account_name=self.account_name,
            resource_group_name=self._resource_group_name,
            default_encryption_scope=container_config.default_encryption_scope,
            deny_encryption_scope_override=container_config.deny_encryption_scope_override,
            metadata=container_config.metadata,
            public_access=container_config.public_access,
            opts=opts
        )
