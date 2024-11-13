## 👩‍💻 Workshop Preparation

If you plan to follow along on the workshop, please **COMPLETE ALL TASKS** before attending!

### Checkout and Update the Workshop Branch

```
git checkout dataphos-workshops

git pull
```

### Install Python

Please make sure you have Python installed ([Windows](https://www.python.org/downloads/windows/), [Linux/UNIX](https://www.python.org/downloads/source/), [macOS](https://www.python.org/downloads/macos/))

**⚠️WARNING⚠️**: install Python version 3.11 or lower, newer Python versions caused problems while using pip.

### Install Dependencies

Create a virtual environment from the `pulumi/` directory:

```
cd pulumi
```

Create the virtual environment using the `-3.XX` flag which explicitly selects the python version to use. For example, if you installed python version `3.10`, run the following command:

```
py -3.10 -m venv .venv
```

Activate the virtual environment.

Windows:

```
.\.venv\Scripts\activate
```

Mac/Linux:

```
source .venv/bin/activate
```

Install package dependencies:

```
py -m pip install -r .\requirements.txt
```

This installation will last anywhere from 10 to 30 minutes. Please proceed to next steps while it installs.

### Configure Cloud Credentials

Authorize access to the cloud where you will deploy the infrastructure using the CLI. Log in to the AzureCLI and Pulumi will automatically use your credentials:

```
az login
```

If you got an error because you don't have `az` installed, please follow the instructions on [this](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) link to install it. After the installation, please restart the terminal and try the command above again.

You need to have access to the [Syntio - Microsoft Azure (Enterprise)](https://portal.azure.com/#@syntio.net/resource/subscriptions/a8330230-b8a0-4839-8650-17faf7ddcc42/overview) subscription. If you don't have access, please create a post in the [Security and Infrastructure](https://teams.microsoft.com/l/channel/19%3A5c191b040ad54297a9e6caa16f918810%40thread.skype/Security%20and%20Infrastructure?groupId=60ba0e91-26c9-47ae-81e9-974956868bbf&tenantId=e27500de-8438-45fb-8228-8bf0cc45248b) channel.

Select the the [Syntio - Microsoft Azure (Enterprise)](https://portal.azure.com/#@syntio.net/resource/subscriptions/a8330230-b8a0-4839-8650-17faf7ddcc42/overview) subscription as the active one with the following command:

```
az account set --subscription a8330230-b8a0-4839-8650-17faf7ddcc42
```

### Install Pulumi

You can follow the official tutorial [here](https://www.pulumi.com/docs/install/) or:

- on Windows, run: `choco install pulumi`
- on Mac, run: `brew install pulumi/tap/pulumi`
- on Linux, run: `curl -fsSL https://get.pulumi.com | sh`

### Log into Pulumi

You need to log in to Pulumi in the CLI. If you don't have an account, please create one by connecting with your GitHub.

```
pulumi login
```

Your workshop preparation ends here!

**Additional Note:**
Windows has a file path length limit (260 characters), which may cause issues with long file paths during installation (particularly the "pulumi_azure_native\m365securityandcompliance\v20210325preview\get_private_link_services_for_o365_management_activity_api.py" file).

To overcome this, enable long path support by editing the Windows registry:

1. Open `regedit` (Registry Editor).
2. Navigate to `Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`.
3. Edit the `LongPathsEnabled` DWORD Value and set it to `1`.
