# dataphos-core

This repository is the starting point for deploying and using Dataphos components. It contains Pulumi deployment scripts that can deploy Dataphos components and the necessary cloud infrastructure, building upon Helm charts that reference pre-built container images for each Dataphos microservice. These scripts and charts enable you to quickly launch Dataphos components in your cloud environment with minimal configuration.

## 📋 About Dataphos

Dataphos is a collection of microservices designed to solve the common issues arising in the current world of Data Engineering. Although each component is designed and developed independently to support the specific needs of existing architectures, Dataphos is built to inevitably come together as a unified ingestion platform, guiding the journey of your data from on-premise systems into the cloud and beyond.

Started in 2020 by battle-hardened industry professionals, Dataphos was built as a solution to the common issues plaguing Event-Driven Architectures:

- How do you transfer data from an on-premise database as a collection of structured records without relying on CDC solutions to merely replicate the database row-by-row?
- How do you ensure that data consumers don’t break due to sudden changes in the underlying schema of the data?
- How do you ensure proper fail-saves exist while using streaming services? How do you replay messages?
- How can you quickly and efficiently build structured Data Lake architectures?

At its core, Dataphos is an accelerator, enabling your engineers to focus on delivering business value by providing pre-built solutions to the common challenges faced in data architectures today. It is designed to integrate seamlessly with your existing infrastructure and scale with your architecture's specific requirements.

## ✅ Prerequisites

* [Python 3](https://www.python.org/downloads/)
* [Pulumi 3](https://www.pulumi.com/docs/install/)

## 👩‍💻 Usage

### Download Helm Charts

The Dataphos Helm charts are located in the [dataphos-helm repository](https://github.com/dataphos/dataphos-helm).

To properly reference the charts during deployment, clone the dataphos-helm repository and copy its contents into the `helm_charts/` directory of the cloned dataphos-core repository.

If you're planning on working with Kafka topics, clone the [strimzi-kafka-operator repository](https://github.com/strimzi/strimzi-kafka-operator/tree/main) and copy the contents of its `helm_charts/` directory to the same directory in the cloned dataphos-core repository.

The contents of the `helm_charts/` directory should look like this:

```
├── helm_charts/
    ├── dataphos-persistor/
    ├── dataphos-schema-registry/
    ├── dataphos-schema-registry-validator/
    └── strimzi-kafka-operator/
```

### Install Dependencies

Create a virtual environment from the `pulumi/` directory and activate it:

```
cd pulumi

py -m venv venv
.\venv\Scripts\activate
```

Install package dependencies:

```
py -m pip install -r .\requirements.txt
```

Installation shouldn't take long, but please be patient as it can take up to 45 minutes, depending on your setup.

**Note:** 
Windows has a file path length limit (260 characters), which may cause issues with long file paths during installation (particularly the "pulumi_azure_native\m365securityandcompliance\v20210325preview\get_private_link_services_for_o365_management_activity_api.py" file).

To overcome this, enable long path support by editing the Windows registry:
1. Open `regedit` (Registry Editor).
2. Navigate to `Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`.
3. Edit the `LongPathsEnabled` DWORD Value and set it to `1`.

### Configure Cloud Credentials

Authorize access to the cloud where you will deploy the infrastructure using the CLI.

#### Azure

Log in to the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and Pulumi will automatically use your credentials:

```
az login
```

#### GCP

Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) and then authorize access with a user account. Next, Pulumi requires default application credentials to interact with your Google Cloud resources, so run the command to obtain those credentials:

```
gcloud auth application-default login
```

You will need to have [gke-gcloud-auth-plugin](https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke) installed for use with kubectl before interacting with the Kubernetes cluster. It can easily be installed by running:

```
gcloud components install gke-gcloud-auth-plugin
```

### Configure Your Stack

You can use a stack configuration template file to quickly deploy and modify example architectures. This repository includes a set of pre-configured templates for different combinations of Dataphos components and cloud providers. The Configuration section contains configuration specifics per infrastructure component and a complete [list of templates](#templates).

To start using a stack template, copy the desired file from the `config_templates/` directory into the `pulumi/` directory. Next, create a new stack to contain your infrastructure configuration. If you’re using a pre-configured stack template, make sure to use the same name for your stack. For example, if you copied `Pulumi.dataphos-gcp-pubsub-dev.yaml` into the `pulumi/` directory, run the following command:

```
pulumi stack init dataphos-gcp-pubsub-dev
```

This will create a new stack named `dataphos-gcp-pubsub-dev` in your project and set it as the active stack.

### Deployment

Preview and deploy infrastructure changes:

```
pulumi up
```

Destroy your infrastructure changes:

```
pulumi destroy
```

For complete Pulumi CLI reference, see: [Pulumi CLI reference](https://www.pulumi.com/docs/cli/).

## ⚙️ Configuration

There are three possible sources of resource configuration values: user configuration in the active stack configuration file, retrieved data from existing resources, and default system-level configuration from the application code.

User configuration will always take precedence over other configuration sources. If there is no special user configuration for a parameter, the retrieved value from the resource’s previous configuration will be used. If there wasn’t any data retrieved for the resource (as it is being created for the first time), the default system-level configuration value will be used instead. The default values for parameters are listed in the appropriate section of the configuration options.

If the configuration references an existing cloud resource, the program will retrieve its data from the cloud provider and import the resource into the active stack instead of creating a new one. If the user configuration values specify any additional parameters that differ from the resource configuration while it has not yet been imported into the stack, the deployment will fail. To modify an existing resource’s configuration, import it into the stack first and then redeploy the infrastructure with the desired changes.

**Note:** Implicit import of an AKS cluster is currently not supported. To use an existing AKS cluster in your infrastructure, set the AKS cluster's `import` configuration option to `true`.

⚠️ **WARNING** ⚠️

Imported resources will **NOT** be retained by default when the infrastructure is destroyed. If you want to retain a resource when the infrastructure is destroyed, you need to explicitly set its `retain` flag to `true` in the active stack's configuration file. Retained resources will not be deleted from the backing cloud provider, but will be removed from the Pulumi state on a `pulumi destroy`.
Azure resource groups and GCP projects are set to be retained by default and can be deleted manually. Be careful if you choose not to retain them, as destroying them will remove **ALL** children resources, even the ones created externally. It is recommended to modify these options only if you are using a dedicated empty project/resource group.

### Global Configuration Options

| Variable                        | Type    | Description                                                                                                    | Default value |
|---------------------------------|---------|----------------------------------------------------------------------------------------------------------------|---------------|
| `namespace`                     | string  | The name of the Kubernetes namespace where Dataphos Helm charts will be deployed to.                           | `dataphos`    |
| `deployPersistor`               | boolean | Whether the Persistor Helm chart should be deployed.                                                           | `false`       |
| `deploySchemaRegistry`          | boolean | Whether the Schema Registry Helm chart should be deployed.                                                     | `false`       |
| `deploySchemaRegistryValidator` | boolean | Whether the Schema Registry Validator Helm chart should be deployed.                                           | `false`       |
| `retainResourceGroups`          | boolean | Whether Azure resource groups should be retained when the infrastructure is destroyed.                         | `true`        |
| `retainProjects`                | boolean | Whether GCP projects should be retained when the infrastructure is destroyed.                                  | `true`        |
| `resourceTags`                  | object  | Set of `key:value` tags attached to all Azure resource groups; or set of labels attached to all GCP resources. |               |

### Product Configuration Options

The `namespace` and `images` options at the top-level of the Helm chart configurations are set by default and do not need to be manually configured.

Cloud-specific variables should not be manually configured. Depending on the configured cloud provider, service accounts with appropriate roles are automatically created and their credentials are used to populate these variables.

| Variable                                       | Type   | Description                                                                                                                                                                                                                                                                      |
|------------------------------------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dataphos-persistor`                           | object | Dataphos Persistor Helm chart configuration. Configuration options are listed in the [dataphos-persistor README file](https://github.com/dataphos/dataphos-helm/blob/master/dataphos-persistor/README.md#configuration).                                                           |
| `dataphos-persistor.persistor`                 | object | The object containing the information on all of the Persistors to be deployed. Configuration options are listed in the [dataphos-persistor README file](https://github.com/dataphos/dataphos-helm/blob/master/dataphos-persistor/README.md#persistor-configuration).               |
| `dataphos-persistor.indexer`                   | object | The object containing the information on all of the indexers to be deployed. Configuration options are listed in the [dataphos-persistor README file](https://github.com/dataphos/dataphos-helm/blob/master/dataphos-persistor/README.md#indexer-configuration).                   |
| `dataphos-persistor.resubmitter`               | object | The object containing the information on all of the resubmitter services to be deployed. Configuration options are listed in the [dataphos-persistor README file](https://github.com/dataphos/dataphos-helm/blob/master/dataphos-persistor/README.md#resubmitter-configuration).   |
| `dataphos-schema-registry`                     | object | Dataphos Schema Registry Helm chart configuration. Configuration options are listed in the [dataphos-schema-registry README file](https://github.com/dataphos/dataphos-helm/blob/master/dataphos-schema-registry/README.md).                                                       |
| `dataphos-schema-registry-validator`           | object | Dataphos Schema Registry Validator Helm chart configuration. Configuration options are listed in the [dataphos-schema-registry-validator README file](https://github.com/dataphos/dataphos-helm/blob/master/dataphos-schema-registry-validator/README.md#configuration).                                      |
| `dataphos-schema-registry-validator.validator` | object | The object containing the information on all of the validators to be deployed. Configuration options are listed in the [dataphos-schema-registry-validator README file](https://github.com/dataphos/dataphos-helm/blob/master/dataphos-schema-registry-validator/README.md#validator-configuration). |


### Provider Configuration Options

The variables listed here are required configuration options by their respective Pulumi providers. Your entire infrastructure should reside on a single cloud platform. Deployment across multiple cloud platforms is currently not fully supported.

#### Azure

| Variable                | Type   | Description                        | Example value |
|-------------------------|--------|------------------------------------|---------------|
| `azure-native:location` | string | The default resource geo-location. | `westeurope`  |

A list of all configuration options for this provider can be found here:
[Azure Native configuration options](https://www.pulumi.com/registry/packages/azure-native/installation-configuration/#configuration-options).

#### GCP

To successfully deploy resources in a GCP project, the appropriate APIs need to be enabled for that project in the API Console. See: [Enable and disable APIs](https://support.google.com/googleapi/answer/6158841).

| Variable      | Type   | Description              | Example value      |
|---------------|--------|--------------------------|--------------------|
| `gcp:project` | string | The default GCP project. | `dataphos-project` |
| `gcp:region`  | string | The default region..     | `europe-west2`     |
| `gcp:zone`    | string | The default zone.        | `europe-west2-a`   |

A list of all configuration options for this provider can be found here:
[GCP configuration options](https://www.pulumi.com/registry/packages/gcp/installation-configuration/#configuration-reference).

### Cluster Configuration Options

The stack configuration `cluster` object is utilized to configure the Kubernetes cluster necessary to deploy the Helm charts that comprise Dataphos products.

| Variable                    | Type    | Description                                                                                                                                                                                    |
|-----------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `cluster`                   | object  | The object containing the general information on the cluster.                                                                                                                                  |
| `cluster.CLUSTER_ID`        | object  | The object representing an individual cluster's configuration.                                                                                                                                 |
| `cluster.CLUSTER_ID.type`   | string  | The type of the managed cluster. Valid values: [`gke`, `aks`].                                                                                                                                 |
| `cluster.CLUSTER_ID.name`   | string  | The name of the managed cluster.                                                                                                                                                               |
| `cluster.CLUSTER_ID.retain` | boolean | If set to true, resource will be retained when infrastructure is destroyed. Retained resources will not be deleted from the backing cloud provider, but will be removed from the Pulumi state. |

#### AKS

| Variable                                                 | Type    | Description                                                                                                                                                                                  | Default value     |
|----------------------------------------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `cluster.CLUSTER_ID.import`                              | boolean | Whether to use an existing AKS cluster instead of creating a new one.<br>**Note:** AKS clusters imported in this way will be retained on destroy, unless its resource group is not retained. | `false`           |
| `cluster.CLUSTER_ID.resourceGroup`                       | string  | The name of the resource group. The name is case insensitive.                                                                                                                                |                   |
| `cluster.CLUSTER_ID.sku`                                 | object  | The managed cluster SKU.                                                                                                                                                                     |                   |
| `cluster.CLUSTER_ID.sku.name`                            | string  | The managed cluster SKU name.                                                                                                                                                                | `Basic`           |
| `cluster.CLUSTER_ID.sku.tier`                            | string  | The managed cluster SKU tier.                                                                                                                                                                | `Free`            |
| `cluster.CLUSTER_ID.dnsPrefix`                           | string  | The cluster DNS prefix. This cannot be updated once the Managed Cluster has been created.                                                                                                    |                   |
| `cluster.CLUSTER_ID.agentPoolProfiles`                   | object  | The agent pool properties.                                                                                                                                                                   |                   |
| `cluster.CLUSTER_ID.agentPoolProfiles.name`              | string  | Windows agent pool names must be 6 characters or less.                                                                                                                                       |                   |
| `cluster.CLUSTER_ID.agentPoolProfiles.count`             | integer | Number of agents (VMs) to host docker containers.                                                                                                                                            | `3`               |
| `cluster.CLUSTER_ID.agentPoolProfiles.enableAutoScaling` | boolean | Whether to enable auto-scaler.                                                                                                                                                               | `false`           |
| `cluster.CLUSTER_ID.agentPoolProfiles.minCount`          | integer | The minimum number of nodes for auto-scaling.                                                                                                                                                | `1`               |
| `cluster.CLUSTER_ID.agentPoolProfiles.maxCount`          | integer | The maximum number of nodes for auto-scaling.                                                                                                                                                | `5`               |
| `cluster.CLUSTER_ID.agentPoolProfiles.vmSize`            | string  | VM size availability varies by region. See: [Supported VM sizes](https://docs.microsoft.com/azure/aks/quotas-skus-regions#supported-vm-sizes)                                                | `Standard_DS2_v2` |
| `cluster.CLUSTER_ID.tags`                                | object  | Set of `key:value` tags attached to the AKS Cluster. This will override the global `resourceTags` configuration option for this resource.                                                    |                   |

#### GKE

| Variable                                                       | Type        | Description                                                                                                                                                                                                        | Default value                                                                                                                                                                                                      |
|----------------------------------------------------------------|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `cluster.CLUSTER_ID.projectID`                                 | string      | The project ID is a unique identifier for a GCP project.                                                                                                                                                           |                                                                                                                                                                                                                    |
| `cluster.CLUSTER_ID.location`                                  | string      | The geo-location where the resource lives.                                                                                                                                                                         |                                                                                                                                                                                                                    |
| `cluster.CLUSTER_ID.initialNodeCount`                          | integer     | The number of nodes to create in this cluster's default node pool.                                                                                                                                                 | `3`                                                                                                                                                                                                                |
| `cluster.CLUSTER_ID.nodeConfigs`                               | object      | Parameters used in creating the default node pool.                                                                                                                                                                 |                                                                                                                                                                                                                    |
| `cluster.CLUSTER_ID.nodeConfig.machineType`                    | string      | The name of a Google Compute Engine machine type.                                                                                                                                                                  | `e2-medium`                                                                                                                                                                                                        |
| `cluster.CLUSTER_ID.clusterAutoscalings`                       | object list | Per-cluster configuration of Node Auto-Provisioning with Cluster Autoscaler to automatically adjust the size of the cluster and create/delete node pools based on the current needs of the cluster's workload.     |                                                                                                                                                                                                                    |
| `cluster.CLUSTER_ID.clusterAutoscalings[0].autoscalingProfile` | string      | Lets you choose whether the cluster autoscaler should optimize for resource utilization or resource availability when deciding to remove nodes from a cluster. Valid values: [`BALANCED`, `OPTIMIZE_UTILIZATION`]. | `BALANCED`                                                                                                                                                                                                         |
| `cluster.CLUSTER_ID.clusterAutoscalings[0].enabled`            | boolean     | Whether node auto-provisioning is enabled.                                                                                                                                                                         | `false`                                                                                                                                                                                                            |
| `cluster.CLUSTER_ID.clusterAutoscalings[0].resourceLimits`     | object list | Global constraints for machine resources in the cluster. Configuring the cpu and memory types is required if node auto-provisioning is enabled.                                                                    | resourceLimits:<br>-&nbsp;resource_type:&nbsp;cpu<br>&nbsp;&nbsp;minimum:&nbsp;1<br>&nbsp;&nbsp;maximum:&nbsp;1<br>-&nbsp;resource_type:&nbsp;memory<br>&nbsp;&nbsp;minimum:&nbsp;1<br>&nbsp;&nbsp;maximum:&nbsp;1 |
| `cluster.CLUSTER_ID.resourceLabels`                            | object      | Set of `key:value` labels attached to the GKE Cluster. This will override the global `resourceTags` configuration option for this resource.                                                                        |                                                                                                                                                                                                                    |

### Broker Configuration Options

The stack configuration `brokers` object is used to set up the key references to be used by the dataphos components to connect to one or more brokers deemed as part of the overall platform infrastructure.

Product configs directly reference brokers by their `BROKER_ID` listed in the broker config. The same applies to `TOPIC_ID` and `SUB_ID` – the keys of those objects are the actual names of the topics and subscriptions used.

| Variable                                                                 | Type    | Description                                                                                                                                                                                    |
|--------------------------------------------------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `brokers`                                                                | object  | The object containing the general information on the brokers.                                                                                                                                  |
| `brokers.BROKER_ID`                                                      | object  | The object representing an individual broker's configuration.                                                                                                                                  |
| `brokers.BROKER_ID.type`                                                 | string  | Denotes the broker's type. Valid values: [`kafka`, `pubsub`, `servicebus`].                                                                                                                    |
| `brokers.BROKER_ID.topics`                                               | object  | The object containing the general information on the topics.                                                                                                                                   |
| `brokers.BROKER_ID.topics.TOPIC_ID`                                      | object  | The object representing an individual topic's configuration.                                                                                                                                   |
| `brokers.BROKER_ID.topics.TOPIC_ID.retain`                               | boolean | If set to true, resource will be retained when infrastructure is destroyed. Retained resources will not be deleted from the backing cloud provider, but will be removed from the Pulumi state. |
| `brokers.BROKER_ID.topics.TOPIC_ID.subscriptions`                        | object  | The object containing topic subscription (consumer group) configuration.                                                                                                                       |
| `brokers.BROKER_ID.topics.TOPIC_ID.subscriptions.SUBSCRIPTION_ID`        | object  | The object representing an individual topic subscription's configuration.                                                                                                                      |
| `brokers.BROKER_ID.topics.TOPIC_ID.subscriptions.SUBSCRIPTION_ID.retain` | boolean | If set to true, resource will be retained when infrastructure is destroyed. Retained resources will not be deleted from the backing cloud provider, but will be removed from the Pulumi state. |

The Azure storage account type. Valid values: [`Storage`, `StorageV2`, `BlobStorage`, `BlockBlobStorage`, `FileStorage`]. The default and recommended value is `BlockBlobStorage`.
#### Azure Service Bus
| Variable                          | Type    | Description                                                                                                                                                                                                           |
|-----------------------------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `brokers.BROKER_ID.azsbNamespace` | string  | The Azure Service Bus namespace name.                                                                                                                                                                                 |
| `brokers.BROKER_ID.resourceGroup` | string  | The Azure Service Bus resource group name.                                                                                                                                                                            |
| `brokers.BROKER_ID.sku`           | object  | The Azure Service Bus namespace SKU properties.                                                                                                                                                                       |
| `brokers.BROKER_ID.sku.name`      | string  | Name of this SKU. Valid values: [`BASIC`, `STANDARD`, `PREMIUM`]. Default value is `STANDARD`.                                                                                                                        |
| `brokers.BROKER_ID.sku.tier`      | string  | The billing tier of this SKU. [`BASIC`, `STANDARD`, `PREMIUM`]. Default value is `STANDARD`.                                                                                                                          |
| `brokers.BROKER_ID.sku.capacity`  | integer | The specified messaging units for the tier. For Premium tier, valid capacities are 1, 2 and 4.                                                                                                                        |
| `brokers.BROKER_ID.tags`          | object  | Set of `key:value` tags attached to the Azure Service Bus namespace. This will override the global `resourceTags` configuration option for this resource.                                                             |
| `brokers.BROKER_ID.retain`        | boolean | If set to true, the Azure Service Bus namespace will be retained when infrastructure is destroyed. Retained resources will not be deleted from the backing cloud provider, but will be removed from the Pulumi state. |

#### Google Cloud Pub/Sub
| Variable                                                                 | Type   | Description                                                                                                                                          |
|--------------------------------------------------------------------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| `brokers.BROKER_ID.projectID`                                            | string | The GCP project ID.                                                                                                                                  |
| `brokers.BROKER_ID.topics.TOPIC_ID.labels`                               | object | Set of `key:value` labels attached to the Pub/Sub topic. This will override the global `resourceTags` configuration option for this resource.        |
| `brokers.BROKER_ID.topics.TOPIC_ID.subscriptions.SUBSCRIPTION_ID.labels` | object | Set of `key:value` labels attached to the Pub/Sub subscription. This will override the global `resourceTags` configuration option for this resource. |

#### Kafka
| Variable                                       | Type    | Description                                                                                                                                                 | Default value   |
|------------------------------------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| `brokers.BROKER_ID.brokerAddr`                 | string  | The Kafka bootstrap server address. Optional. If omitted or empty, a new Strimzi Kafka cluster operator and cluster will be deployed with default settings. |                 |
| `brokers.BROKER_ID.clusterName`                | string  | The name of the Strimzi Kafka cluster custom Kubernetes resource.                                                                                           | `kafka-cluster` |
| `brokers.BROKER_ID.clusterNamespace`           | string  | The Kubernetes namespace where the cluster will be deployed.                                                                                                | `kafka-cluster` |
| `brokers.BROKER_ID.topics.TOPIC_ID.partitions` | integer | Number of partitions for a specific topic.                                                                                                                  | `3`             |
| `brokers.BROKER_ID.topics.TOPIC_ID.replicas`   | integer | Number of replicas for a specific topic.                                                                                                                    | `1`             |

### Storage Configuration Options

The stack configuration `storage` object is used to set up the key references to be used by the dataphos components to connect to one or more storage destinations deemed as part of the overall platform infrastructure.

Product configs directly reference storage components by their `STORAGE_ID` listed in the storage config. The same applies to `BUCKET_ID` – the keys of those objects are the actual names of the buckets used.

| Variable                                      | Type    | Description                                                                                                                                                                                    |
|-----------------------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `storage`                                     | object  | The object containing the general information on the storage services.                                                                                                                         |
| `storage.STORAGE_ID`                          | object  | The object representing an individual storage destination configuration.                                                                                                                       |
| `storage.STORAGE_ID.type`                     | string  | Denotes the storage type. Valid values: [`abs`, `gcs`].                                                                                                                                        |
| `storage.STORAGE_ID.buckets`                  | object  | The object containing the general information on the buckets.                                                                                                                                  |
| `storage.STORAGE_ID.buckets.BUCKET_ID`        | object  | The object representing an individual bucket.                                                                                                                                                  |
| `storage.STORAGE_ID.buckets.BUCKET_ID.retain` | boolean | If set to true, resource will be retained when infrastructure is destroyed. Retained resources will not be deleted from the backing cloud provider, but will be removed from the Pulumi state. |

#### Azure Blob Storage
| Variable                              | Type    | Description                                                                                                                                                                                                     |
|---------------------------------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `storage.STORAGE_ID.accountStorageID` | string  | The Azure storage account name.                                                                                                                                                                                 |
| `storage.STORAGE_ID.resourceGroup`    | string  | The Azure resource group name.                                                                                                                                                                                  |
| `storage.STORAGE_ID.kind`             | string  | The Azure storage account type. Valid values: [`Storage`, `StorageV2`, `BlobStorage`, `BlockBlobStorage`, `FileStorage`]. The default and recommended value is `BlockBlobStorage`.                              |
| `storage.STORAGE_ID.tags`             | object  | Set of `key:value` tags attached to the Azure storage account. This will override the global `resourceTags` configuration option for this resource.                                                             |
| `storage.STORAGE_ID.retain`           | boolean | If set to true, the Azure storage account will be retained when infrastructure is destroyed. Retained resources will not be deleted from the backing cloud provider, but will be removed from the Pulumi state. |

#### Google Cloud Storage
| Variable                                      | Type   | Description                                                                                                                                |
|-----------------------------------------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `storage.STORAGE_ID.projectID`                | string | The GCP project ID.                                                                                                                        |
| `storage.STORAGE_ID.buckets.BUCKET_ID.labels` | object | Set of `key:value` labels attached to the GCS bucket. This will override the global `resourceTags` configuration option for this resource. |

**Note:** The `BUCKET_ID` used as the name of a GCS bucket must be globally unique on GCP. If you encounter deployment issues because a bucket of the same name already exists, pick a unique name and make sure to update the bucket reference in your Pulumi config to the same `BUCKET_ID`. Make sure to update the `persistor.storageTargetID` that references it as well.

### Created Resources

A full list of infrastructure resource types that can be created with the provided scripts is provided in this section, excluding Kubernetes resources created by Helm charts.

The following table lists resource types that are named by the user in the stack configuration file.
The `Name Field` column contains the stack configuration field that determines the name of the resource.
The `Cloud Platform` column is populated if the resource type is specific to a certain cloud provider.

| Cloud Platform | Resource Type         | Name Field                                                                                                   |
|----------------|-----------------------|--------------------------------------------------------------------------------------------------------------|
| Azure          | Resource Group        | `cluster.CLUSTER_ID.resourceGroup` or `storage.STORAGE_ID.resourceGroup` or `broker.BROKER_ID.resourceGroup` |
| Azure, GCP     | Kubernetes cluster    | `cluster.CLUSTER_ID.name` or `cluster.CLUSTER_ID`                                                            |
| Azure          | Service Bus Namespace | `brokers.BROKER_ID.azsbNamespace` or `brokers.BROKER_ID`                                                     |
| Azure, GCP     | Message Broker Topic  | `brokers.BROKER_ID.topics.TOPIC_ID`                                                                          |
| Azure, GCP     | Topic Subscription    | `brokers.BROKER_ID.topics.TOPIC_ID.subscriptions.SUB_ID`                                                     |
| Azure          | Storage Account       | `storage.STORAGE_ID.accountStorageID` or `storage.STORAGE_ID`                                                |
| Azure, GCP     | Storage Bucket        | `storage.STORAGE_ID.buckets.BUCKET_ID`                                                                       |

The table below lists resources that are named using certain fields from the stack configuration file, but the user cannot name them explicitly.
Service Accounts are created per app instance and cannot be imported.

| Cloud Platform | Resource Type                     | Resource Name                              |
|----------------|-----------------------------------|--------------------------------------------|
| Azure          | Application Registration          | `[app_id]`-app                             |
| Azure          | Application Registration password | `[app_id]`-app-password                    |
| Azure          | Service Principal                 | `[app_id]`-servicePrincipal                |
| Azure          | Service Principal Role Assignment | `[app_id]`-`[resource_name]`-`[role_name]` |
| GCP            | Service Account                   | `[app_id]`-sa                              |
| GCP            | Service Account secret key        | `[app_id]`-sa-key                          |
| GCP            | IAM Member                        | `[app_id]`-`[resource_name]`-`[role_name]` |

### Templates

| Template Name                    | Description                                                                                                                                                      |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dataphos-azure-kafka-dev`       | Deploys all Dataphos products and supporting cloud infrastructure on Azure, using Strimzi Kafka as the message broker.                                           |
| `dataphos-azure-sb-dev`          | Deploys all Dataphos products and supporting cloud infrastructure on Azure, using Azure Service Bus as the message broker.                                       |
| `dataphos-gcp-kafka-dev`         | Deploys all Dataphos products and supporting cloud infrastructure on GCP, using Strimzi Kafka as the message broker.                                             |
| `dataphos-gcp-pubsub-dev`        | Deploys all Dataphos products and supporting cloud infrastructure on GCP, using Google Cloud Pub/Sub as the message broker.                                      |
| `persistor-azure-kafka-dev`      | Deploys the Persistor product and supporting cloud infrastructure on Azure, using Strimzi Kafka as the message broker.                                           |
| `persistor-azure-sb-dev`         | Deploys the Persistor product and supporting cloud infrastructure on Azure, using Azure Service Bus as the message broker.                                       |
| `persistor-gcp-kafka-dev`        | Deploys the Persistor product and supporting cloud infrastructure on GCP, using Strimzi Kafka as the message broker.                                             |
| `persistor-gcp-pubsub-dev`       | Deploys the Persistor product and supporting cloud infrastructure on GCP, using Google Cloud Pub/Sub as the message broker.                                      |
| `schemaregistry-azure-kafka-dev` | Deploys the Schema Registry and Schema Registry Validator products and supporting cloud infrastructure on Azure, using Strimzi Kafka as the message broker.      |
| `schemaregistry-azure-sb-dev`    | Deploys the Schema Registry and Schema Registry Validator products and supporting cloud infrastructure on Azure, using Azure Service Bus as the message broker.  |
| `schemaregistry-gcp-kafka-dev`   | Deploys the Schema Registry and Schema Registry Validator products and supporting cloud infrastructure on GCP, using Strimzi Kafka as the message broker.        |
| `schemaregistry-gcp-pubsub-dev`  | Deploys the Schema Registry and Schema Registry Validator products and supporting cloud infrastructure on GCP, using Google Cloud Pub/Sub as the message broker. |
