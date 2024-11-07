# Dataphos Schema Registry Validator

The Helm Chart for the Dataphos Schema Registry Validator component.

## Configuration

Below is the list of configurable options in the `values.yaml` file.

| Variable              | Type    | Description                                                                     | Default                                              |
| --------------------- | ------- | ------------------------------------------------------------------------------- | ---------------------------------------------------- |
| namespace             | string  | The namespace to deploy the Schema Registry into.                               | `dataphos`                                           |
| images                | object  | Docker images to use for each of the individual Schema Registry sub-components. |                                                      |
| images.validator      | string  | The Schema Registry Validator image.                                            | `syntioinc/dataphos-schema-registry-validator:1.0.0` |
| images.xmlValidator   | string  | The XML Validator image.                                                        | `syntioinc/dataphos-schema-registry-xml-val:1.0.0`   |
| images.csvValidator   | string  | The CSV Validator image.                                                        | `syntioinc/dataphos-schema-registry-csv-val:1.0.0`   |
| xmlValidator          | object  | The XML Validator configuration.                                                |                                                      |
| xmlValidator.enable   | boolean | Determines whether the XML Validator should be enabled.                         | `true`                                               |
| xmlValidator.replicas | integer | The number of XML Validator replicas.                                           | `1`                                                  |
| csvValidator          | object  | The CSV Validator configuration.                                                |                                                      |
| csvValidator.enable   | boolean | Determines whether the CSV Validator should be enabled.                         | `true`                                               |
| csvValidator.replicas | integer | The number of CSV Validator replicas.                                           | `1`                                                  |
| schemaRegistryURL     | string  | The link to the Schema Registry component.                                      | `http://schema-registry-svc:8080`                    |

### Broker Configuration

The `values.yaml` file contains a `brokers` object used to set up the key references to be used by the Validators to
connect to one or more brokers deemed as part of the overall platform infrastructure.

| Variable                           | Type   | Description                                                                                                     | Applicable If          |
| ---------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------- | ---------------------- |
| brokers                            | object | The object containing the general information on the brokers the Validator service will want to associate with. |                        |
| brokers.BROKER_ID                  | object | The object representing an individual broker's configuration.                                                   |                        |
| brokers.BROKER_ID.type             | string | Denotes the broker's type.                                                                                      |                        |
| brokers.BROKER_ID.connectionString | string | The Azure Service Bus Namespace connection string.                                                              | `type` == `servicebus` |
| brokers.BROKER_ID.projectID        | string | The GCP project ID.                                                                                             | `type` == `pubsub`     |
| brokers.BROKER_ID.brokerAddr       | string | The Kafka bootstrap server address.                                                                             | `type` == `kafka`      |

### Validator Configuration

The `values.yaml` file contains a `validator` object used to configure one or more Validators to be deployed as part of
the release, explicitly referencing brokers defined in the previous section.

| Variable                              | Type   | Description                                                                                                                           | Applicable If                        |
| ------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| validator                             | object | The object containing the information on all of the Validators to be deployed as part of the Helm installation.                       |                                      |
| validator.VAL_ID                      | object | The object representing the individual Validator's configuration.                                                                     |                                      |
| validator.VAL_ID.broker               | string | Reference to the broker messages are pulled FROM.                                                                                     |                                      |
| validator.VAL_ID.destinationBroker    | string | Reference to the broker messages are sent TO.                                                                                         |                                      |
| validator.VAL_ID.topic                | string | The topic the messages are pulled FROM.                                                                                               |                                      |
| validator.VAL_ID.consumerID           | string | The consumer identifier (subscription, consumer group, etc).                                                                          |                                      |
| validator.VAL_ID.validTopic           | string | The topic VALID messages are sent TO.                                                                                                 |                                      |
| validator.VAL_ID.deadletterTopic      | string | The topic INVALID messages are sent TO.                                                                                               |                                      |
| validator.VAL_ID.replicas             | string | The number of replicas of a given Validator instance to pull/process messages simultaneously.                                         |                                      |
| validator.VAL_ID.serviceAccountSecret | string | The reference to a secret that contains a `key.json` key and the contents of a Google Service Account JSON file as its contents.      | `brokers.BROKER_ID.type` == `pubsub` |
| validator.VAL_ID.serviceAccountKey    | string | A Google Service Account private key in JSON format, base64 encoded. Used to create a new `serviceAccountSecret` secret, if provided. | `brokers.BROKER_ID.type` == `pubsub` |

## Created Resources

Below is the list of resources created by this chart.

| Resource type | Resource name                  |
| ------------- | ------------------------------ |
| Deployment    | scval-`[scval_id]`             |
| Service       | scval-`[scval_id]`-metrics-svc |
| ConfigMap     | scval-`[scval_id]`-config      |
| Secret        | `[scval_id]`-gcp-sa-key        |
| Deployment    | validator-csv                  |
| Service       | validator-csv-svc              |
| Deployment    | validator-xml                  |
| Service       | validator-xml-svc              |
