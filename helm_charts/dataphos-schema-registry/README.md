# Dataphos Schema Registry

The Helm Chart for the Dataphos Schema Registry component.

## Configuration

Below is the list of configurable options in the `values.yaml` file.

| Variable                    | Type    | Description                                                                     | Default                                                  |
| --------------------------- | ------- | ------------------------------------------------------------------------------- | -------------------------------------------------------- |
| namespace                   | string  | The namespace to deploy the Schema Registry into.                               | `dataphos`                                               |
| images                      | object  | Docker images to use for each of the individual Schema Registry sub-components. |                                                          |
| images.initdb               | string  | Initdb Docker image.                                                            | `syntioinc/dataphos-schema-registry-initdb:1.0.0`        |
| images.registry             | string  | The Schema Registry image.                                                      | `syntioinc/dataphos-schema-registry-api:1.0.0`           |
| images.compatibilityChecker | string  | The Compatibility checker image.                                                | `syntioinc/dataphos-schema-registry-compatibility:1.0.0` |
| images.validityChecker      | string  | The Validity Checker image.                                                     | `syntioinc/dataphos-schema-registry-validity:1.0.0`      |
| registryReplicas            | integer | The number of replicas of the Schema Registry service.                          | `1`                                                      |
| registrySvcName             | string  | The name of the Schema Registry service.                                        | `schema-registry-svc`                                    |
| database                    | object  | The Schema History database configuration object.                               |                                                          |
| database.name               | string  | History database name.                                                          | `postgres`                                               |
| database.username           | string  | History database username.                                                      | `postgres`                                               |
| database.password           | string  | History database password.                                                      | `POSTGRES_PASSWORD`                                      |

## Created Resources

Below is the list of resources created by this chart.

| Resource type           | Resource name                        |
| ----------------------- | ------------------------------------ |
| Deployment              | schema-registry                      |
| Service                 | schema-registry-svc                  |
| Secret                  | schema-registry-secret               |
| StatefulSet             | schema-history                       |
| Persistent Volume Claim | schema-history-disk-schema-history-0 |
| Service                 | schema-history-svc                   |
| Secret                  | schema-history-secret                |
