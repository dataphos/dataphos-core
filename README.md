## ✅ Prerequisites

1. [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
1. [Python](https://www.python.org/downloads/)
   - ⚠️WARNING: install Python version 3.11 or lower, newer Python versions caused problems while using pip
1. Pulumi - you can follow the official tutorial [here](https://www.pulumi.com/docs/install/) or:
   - on Windows, run: `choco install pulumi`
   - on Mac, run: `brew install pulumi/tap/pulumi`
   - on Linux, run: `curl -fsSL https://get.pulumi.com | sh`
1. You need to log in to Pulumi in the CLI using the `pulumi login` command (create an account if you don't have one)
1. You need to have access to the [Syntio - Microsoft Azure (Enterprise)](https://portal.azure.com/#@syntio.net/resource/subscriptions/a8330230-b8a0-4839-8650-17faf7ddcc42/overview) subscription

## 👩‍💻 Workshop Preparation

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
