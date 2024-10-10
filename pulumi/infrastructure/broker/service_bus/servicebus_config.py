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
