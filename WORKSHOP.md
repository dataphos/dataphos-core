## 👩‍💻 The Workshop

### Configure Your Stack

You can use a stack configuration template file to quickly deploy and modify desired architectures. This repository includes the [Pulumi.workshop-participant-config.yaml](./pulumi/Pulumi.workshop-participant-config.yaml) file, a set of pre-configured cloud resources and Dataphos components that are going to be used on the Workshop. All of these resources have a `<participant_identification>` prefix. Please change all prefix occurrences to your identificator

In the [Pulumi.workshop-participant-config.yaml](./pulumi/Pulumi.workshop-participant-config.yaml) file, there are a bunch

Create a new stack to contain your infrastructure configuration. If you’re using a pre-configured stack template, make sure to use the same name for your stack. For example, if you copied `Pulumi.dataphos-gcp-pubsub-dev.yaml` into the `pulumi/` directory, run the following command:

```
pulumi stack init dataphos-gcp-pubsub-dev
```

This will create a new stack named `dataphos-gcp-pubsub-dev` in your project and set it as the active stack.
