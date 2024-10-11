# Copyright 2024 Syntio Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

account_properties = {
    "location": None,
    "kind": "BlockBlobStorage",
    "allowBlobPublicAccess": None,
    "allowCrossTenantReplication": None,
    "allowSharedKeyAccess": None,
    "defaultToOAuthAuthentication": None,
    "dnsEndpointType": None,
    "enableHttpsTrafficOnly": None,
    "enableNfsV3": None,
    "isHnsEnabled": None,
    "minimumTlsVersion": "TLS1_2",
    "largeFileSharesState": None,
    "accessTier": None,
    "publicNetworkAccess": None,
    "sku": {
        "name": "Premium_LRS",
    },
    "encryption": {
        "services": {
            "blob": {},
            "file": {},
        },
        "keySource": None,
        "requireInfrastructureEncryption": None,
    },
    "networkRuleSet": {
        "bypass": None,
        "defaultAction": None,
    },
    "tags": None,
}

container_properties = {
    "defaultEncryptionScope": None,
    "denyEncryptionScopeOverride": None,
    "metadata": None,
    "publicAccess": None,
}
