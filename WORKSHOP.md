## 👩‍💻 The Workshop

### 1. Task: Stack Configuration

1. Open the [Pulumi.workshop-participant-config.yaml](./pulumi/Pulumi.workshop-participant-config.yaml) file
1. Resources and components have a `<participant_identification>` prefix. Please change all prefix occurrences to your identificator (name and surname would be optimal, lowercase, without any special characters and whitespaces). For example: `robertdakovic-valid-topic`

### 2. Task: Stack Initialization

1. Create a new Pulumi stack to contain your infrastructure configuration:

   ```
   pulumi stack init workshop-participant-config
   ```

   This will create a new stack named `workshop-participant-config` in your project and set it as the active stack.

1. Run the following command:

   ```
   pulumi stack ls
   ```

   The expected output is a list of stacks, or in your case just one stack, with an asterix at the end signaling its the current active stack.

### 3. Task: Deployment

1. Preview and deploy infrastructure changes:

   ```
   pulumi up
   ```
