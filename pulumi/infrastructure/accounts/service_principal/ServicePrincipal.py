from pulumi import ResourceOptions
from pulumi_azure_native import authorization
import pulumi_azuread as azuread

from infrastructure.broker.service_bus.ServiceBusMessageBroker import ServiceBusMessageBroker
from infrastructure.storage.abs.AzureBlobStorage import AzureBlobStorage
from infrastructure.accounts.AbstractAccount import AbstractAccount
from infrastructure.accounts.AccountRoleScope import AccountRoleScope
import infrastructure.accounts.service_principal.service_principal_config as config


class ServicePrincipal(AbstractAccount):
    def __init__(self, app_id: str, parent):
        self._parent = parent

        owner_id = azuread.get_client_config().object_id
        self._service_principal, self._client_secret = self._create_service_principal(app_id, owner_id)
        self._tenant_id = self._service_principal.application_tenant_id
        self._client_id = self._service_principal.application_id
        self._object_id = self._service_principal.object_id
        self._app_id = app_id

    # interface methods
    def add_broker_role(self, broker: ServiceBusMessageBroker, role_config: dict):
        role_definition = config.ROLE_DEFINITIONS.get(role_config["roleID"])
        if role_definition is None: return

        role_scope = role_config["scope"]
        if role_scope == AccountRoleScope.RESOURCE:
            topic_name = role_config["topic"]
            topic = broker.topics[topic_name]
            self._add_role_assignment(role_definition, scope=topic.id, resource_name=topic_name)

            subscription_name = role_config.get("consumerID")
            if not subscription_name: return
            subscription = broker.subscriptions[topic_name][subscription_name]
            self._add_role_assignment(role_definition, scope=subscription.id, resource_name=subscription_name)

        elif role_scope == AccountRoleScope.PROJECT:
            broker_namespace_name = broker.namespace_name
            broker_namespace = broker.namespace
            self._add_role_assignment(role_definition, scope=broker_namespace.id, resource_name=broker_namespace_name)

    def add_storage_role(self, storage: AzureBlobStorage, role_config: dict):
        role_definition = config.ROLE_DEFINITIONS.get(role_config["roleID"])
        if role_definition is None: return

        role_scope = role_config["scope"]
        if role_scope == AccountRoleScope.RESOURCE:
            container_name = role_config["storageTargetID"]
            container = storage.containers[container_name]
            self._add_role_assignment(role_definition, scope=container.id, resource_name=container_name)
        elif role_scope == AccountRoleScope.PROJECT:
            storage_account_name = storage.account_name
            storage_account = storage.storage_account
            self._add_role_assignment(role_definition, scope=storage_account.id, resource_name=storage_account_name)

    def export_config(self):
        account_config = {
            "clientID": self._client_id,
            "clientSecret": self._client_secret,
            "tenantID": self._tenant_id,
        }
        return account_config

    # internal methods
    def _create_service_principal(self, app_id: str, owner_id: str):
        app = azuread.Application(app_id,
            display_name=f"{app_id}-app",
            owners=[owner_id],
            opts=ResourceOptions(parent=self._parent))

        service_principal = azuread.ServicePrincipal(f"{app_id}-servicePrincipal",
            application_id=app.application_id,
            app_role_assignment_required=False,
            owners=[owner_id],
            opts=ResourceOptions(parent=app))

        app_password = azuread.ApplicationPassword(f"{app_id}_secret", display_name=f"{app_id}-app-password", application_object_id=app.object_id, opts=ResourceOptions(parent=app))
        client_secret = app_password.value
        return service_principal, client_secret

    def _add_role_assignment(self, role_definition, scope, resource_name):
        role_name = role_definition["name"].replace(" ", "")
        role_id = role_definition["id"]

        authorization.RoleAssignment(
            f"{self._app_id}-{resource_name}-{role_name}",
            principal_id=self._object_id,
            principal_type=authorization.PrincipalType.SERVICE_PRINCIPAL,
            role_definition_id=f"/providers/Microsoft.Authorization/roleDefinitions/{role_id}",
            scope=scope,
            opts=ResourceOptions(parent=self._service_principal)
        )
