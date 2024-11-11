## 👩‍💻 The Workshop

### 1. Task: Stack Configuration

You can use a stack configuration template file to quickly deploy and modify desired architectures. This repository includes the [Pulumi.workshop-participant-config.yaml](./pulumi/Pulumi.workshop-participant-config.yaml) file, a set of pre-configured cloud resources and Dataphos components that are going to be used on the Workshop. All of these resources have a `<participant_identification>` prefix. Please change all prefix occurrences to your identificator (name and surname would be optimal, lowercase, without any special characters and whitespaces). For example: `robertdakovic-valid-topic`

Create a new Pulumi stack to contain your infrastructure configuration.You’re using a pre-configured Workshop stack template, make sure to use the same name for your stack. Run the following command:

```
pulumi stack init workshop-participant-config
```

This will create a new stack named `workshop-participant-config` in your project and set it as the active stack.
