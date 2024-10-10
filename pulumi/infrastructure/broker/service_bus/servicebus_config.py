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

namespace_properties = {
    "location": None,
    "sku": {
        "name": "STANDARD",
        "tier": "STANDARD",
        "capacity": None,
    },
    "disableLocalAuth": None,
    "minimumTlsVersion": None,
    "zoneRedundant": None,
    "tags": None,
}

topic_properties = {
    "autoDeleteOnIdle": None,
    "defaultMessageTimeToLive": None,
    "duplicateDetectionHistoryTimeWindow": None,
    "enableBatchedOperations": None,
    "enableExpress": None,
    "enablePartitioning": None,
    "maxSizeInMegabytes": None,
    "requiresDuplicateDetection": None,
    "status": None,
    "supportOrdering": None,
    "maxMessageSizeInKilobytes": None,
}

subscription_properties = {
    "autoDeleteOnIdle": None,
    "deadLetteringOnFilterEvaluationExceptions": None,
    "deadLetteringOnMessageExpiration": None,
    "defaultMessageTimeToLive": None,
    "duplicateDetectionHistoryTimeWindow": None,
    "enableBatchedOperations": None,
    "forwardDeadLetteredMessagesTo": None,
    "forwardTo": None,
    "lockDuration": "PT5M",
    "maxDeliveryCount": 2000,
    "requiresSession": None,
    "status": None,
    "isClientAffine": None,
}
