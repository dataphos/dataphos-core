from pulumi import ComponentResource, ResourceOptions

from infrastructure.platform.Platform import Platform
from infrastructure.platform.PlatformID import PlatformID
from infrastructure.accounts.AbstractAccount import AbstractAccount
from infrastructure.accounts.service_principal.ServicePrincipal import ServicePrincipal
from infrastructure.accounts.service_account.ServiceAccount import ServiceAccount
from infrastructure.broker.AbstractMessageBroker import AbstractMessageBroker
from infrastructure.storage.AbstractStorage import AbstractStorage


class Account(ComponentResource, AbstractAccount):

    def __init__(self, app_id: str, account_config: dict, platform: Platform) -> None:
        resource_type = 'dataphos:infrastructure:Account'
        resource_name = f"{app_id}-account"
        workspace = platform.get_workspace(account_config)
        opts = ResourceOptions(parent=workspace)
        super().__init__(resource_type, resource_name, None, opts)

        platform = account_config["platform"]
        if platform == PlatformID.AZURE:
            self._account_instance = ServicePrincipal(app_id, parent=self)
        elif platform == PlatformID.GCP:
            self._account_instance = ServiceAccount(app_id, project=workspace, parent=self)

    def add_broker_role(self, broker: AbstractMessageBroker, role_config: dict):
        return self._account_instance.add_broker_role(broker, role_config)

    def add_storage_role(self, storage: AbstractStorage, role_config: dict):
        return self._account_instance.add_storage_role(storage, role_config)

    def export_config(self):
        return self._account_instance.export_config()
