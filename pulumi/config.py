import pulumi

from infrastructure.accounts.AccountRoleID import AccountRoleID
from infrastructure.accounts.AccountRoleScope import AccountRoleScope
from infrastructure.platform.Platform import Platform
from infrastructure.platform.PlatformID import PlatformID


def add_broker_config(chart_config, broker_id):
    broker_config = chart_config["brokers"].get(broker_id)
    if broker_config is None:
        chart_config["brokers"][broker_id] = {}
        chart_config["brokers"][broker_id]["type"] = brokers[broker_id]["type"]


def add_storage_config(chart_config, storage_id):
    storage_config = chart_config["storage"].get(storage_id)
    if storage_config is None:
        chart_config["storage"][storage_id] = {}
        chart_config["storage"][storage_id]["type"] = storage[storage_id]["type"]


class AccountConfig:

    def __init__(self, instance_id: str, instance_config: dict, resource_config: dict):
        self.instance_id = instance_id
        self.instance_config = instance_config
        self.account_config = { "roles": [] }
        # get default platform and workspace from resource config
        self.platform = Platform.get_platform(resource_config["type"])
        workspace_key = Platform.get_workspace_key(self.platform)
        workspace = resource_config.get(workspace_key)
        self.account_config["platform"] = self.platform
        self.account_config[workspace_key] = workspace

    def add_broker_role(self, role_id, role_scope, broker_id, topic_id=None, sub_key=None):
        if Platform.get_platform(brokers[broker_id]["type"]) == PlatformID.NONE: return
        role = {
            "roleID": role_id,
            "scope": role_scope,
            "broker": broker_id,
        }
        if topic_id: role["topic"] = topic_id
        if sub_key: role["consumerID"] = self.instance_config[sub_key]
        self.account_config["roles"].append(role)
        # always add broker viewer role
        role = dict(role)
        role["roleID"] = AccountRoleID.BROKER_VIEWER
        self.account_config["roles"].append(role)

    def add_storage_role(self, role_id, role_scope, storage_id, bucket_key=None):
        role = {
            "roleID": role_id,
            "scope": role_scope,
            "storage": storage_id,
        }
        if bucket_key: role["storageTargetID"] = self.instance_config[bucket_key]
        self.account_config["roles"].append(role)


stack_name = pulumi.get_stack()

config = pulumi.Config()

# global config
retain_projects = config.get_bool("retainProjects", True)
retain_resource_groups = config.get_bool("retainResourceGroups", True)
resource_tags = config.get_object("resourceTags")

# infrastructure config
cluster = config.get_object("cluster")
brokers = config.get_object("brokers", {})
storage = config.get_object("storage", {})
accounts = {}

# product config
namespace = config.get("namespace", "dataphos")
deploy_schema_registry = config.get_bool("deploySchemaRegistry", False)
deploy_schema_registry_validator = config.get_bool("deploySchemaRegistryValidator", False)
deploy_persistor = config.get_bool("deployPersistor", False)

# schema registry config
if deploy_schema_registry:
    schema_registry_chart_config = config.get_object("dataphos-schema-registry")

# schema registry validator config
if deploy_schema_registry_validator:
    schema_registry_validator_chart_config = config.get_object("dataphos-schema-registry-validator")
    schema_registry_validator_chart_config["brokers"] = {}

    for instance_id, instance_config in schema_registry_validator_chart_config["validator"].items():
        # input broker config
        broker_id = instance_config["broker"]
        add_broker_config(schema_registry_validator_chart_config, broker_id)

        account = AccountConfig(instance_id, instance_config, resource_config=brokers[broker_id])
        if account.platform == PlatformID.NONE: continue
        accounts[instance_id] = account.account_config

        account.add_broker_role(AccountRoleID.BROKER_SUBSCRIBER, AccountRoleScope.RESOURCE, broker_id, instance_config["topic"], "consumerID")

        # destination broker config
        dest_broker_id = instance_config["destinationBroker"]
        add_broker_config(schema_registry_validator_chart_config, dest_broker_id)
        account.add_broker_role(AccountRoleID.BROKER_PUBLISHER, AccountRoleScope.RESOURCE, dest_broker_id, instance_config["validTopic"])
        account.add_broker_role(AccountRoleID.BROKER_PUBLISHER, AccountRoleScope.RESOURCE, dest_broker_id, instance_config["deadletterTopic"])

# persistor config
if deploy_persistor:
    persistor_chart_config = config.get_object("dataphos-persistor")
    persistor_chart_config["brokers"] = {}
    persistor_chart_config["storage"] = {}

    for instance_id, instance_config in persistor_chart_config["persistor"].items():
        # storage config
        storage_id = instance_config["storage"]
        add_storage_config(persistor_chart_config, storage_id)

        account = AccountConfig(instance_id, instance_config, resource_config=storage[storage_id])
        accounts[instance_id] = account.account_config

        account.add_storage_role(AccountRoleID.STORAGE_WRITER, AccountRoleScope.RESOURCE, storage_id, "storageTargetID")

        # input broker config
        broker_id = instance_config["broker"]
        add_broker_config(persistor_chart_config, broker_id)
        account.add_broker_role(AccountRoleID.BROKER_SUBSCRIBER, AccountRoleScope.RESOURCE, broker_id, instance_config["topic"], "consumerID")

        # indexer broker config
        indexer_ref = instance_config.get("indexer")
        if indexer_ref:
            idx_instance_config = persistor_chart_config["indexer"][indexer_ref]
            idx_broker_id = idx_instance_config["broker"]
            account.add_broker_role(AccountRoleID.BROKER_PUBLISHER, AccountRoleScope.RESOURCE, idx_broker_id, idx_instance_config["topic"])

        # deadletter broker config
        dl_topic = instance_config.get("deadletterTopic")
        if dl_topic:
            idx_broker_id = idx_broker_id if indexer_ref else None
            dl_broker_id = idx_broker_id or instance_config.get("deadletterBroker")
            account.add_broker_role(AccountRoleID.BROKER_PUBLISHER, AccountRoleScope.RESOURCE, dl_broker_id, dl_topic)

    # indexer config
    indexer_config = persistor_chart_config.get("indexer")
    if indexer_config:
        for instance_id, instance_config in indexer_config.items():
            # broker config
            broker_id = instance_config["broker"]
            add_broker_config(persistor_chart_config, broker_id)

            account = AccountConfig(instance_id, instance_config, resource_config=brokers[broker_id])
            if account.platform == PlatformID.NONE: continue
            accounts[instance_id] = account.account_config

            account.add_broker_role(AccountRoleID.BROKER_SUBSCRIBER, AccountRoleScope.RESOURCE, broker_id, instance_config["topic"], "consumerID")

            dl_topic = instance_config.get("deadletterTopic")
            if dl_topic:
                account.add_broker_role(AccountRoleID.BROKER_PUBLISHER, AccountRoleScope.RESOURCE, broker_id, dl_topic)

    # resubmitter config
    resubmitter_config = persistor_chart_config.get("resubmitter")
    if resubmitter_config:
        for instance_id, instance_config in resubmitter_config.items():
            # storage config
            storage_id = instance_config["storage"]
            add_storage_config(persistor_chart_config, storage_id)

            account = AccountConfig(instance_id, instance_config, resource_config=storage[storage_id])
            accounts[instance_id] = account.account_config

            account.add_storage_role(AccountRoleID.STORAGE_READER, AccountRoleScope.PROJECT, storage_id)

            # broker config
            broker_id = instance_config["broker"]
            add_broker_config(persistor_chart_config, broker_id)
            account.add_broker_role(AccountRoleID.BROKER_PUBLISHER, AccountRoleScope.PROJECT, broker_id)
