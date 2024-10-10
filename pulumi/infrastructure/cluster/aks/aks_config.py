cluster_properties = {
    "location": None,
    "disableLocalAccounts": None, # False
    "enableRbac": None, # True
    "kubernetesVersion": None,
    "nodeResourceGroup": None, # MC_<rg_name>_<cluster_name>_<location>
    "sku": {
        "name": "Base",
        "tier": "Free",
    },
    "dnsPrefix": None,
    "agentPoolProfiles": [{
        "name": "default", # agentpool
        "count": 3,
        "enableAutoScaling": False,
        "minCount": 1,
        "maxCount": 5,
        "enableNodePublicIp": False,
        "mode": "System",
        "osType": "Linux",
        "osDiskSizeGb": 30,
        "type": "VirtualMachineScaleSets",
        "vmSize": "Standard_DS2_v2",
        "tags": None,
    }],
    "networkProfile": {
        "networkPlugin": "azure", # [azure, kubenet]
    },
    "addonProfiles": {},
    "autoScalerProfile": {},
    "apiServerAccessProfile": {
        "enablePrivateCluster": False,
    },
    "autoUpgradeProfile": {},
    "identityProfile": {},
    "servicePrincipalProfile": None,
    "tags": None,
}
