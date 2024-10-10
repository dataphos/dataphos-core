topic_properties = {
    "messageRetentionDuration": None,
    "schemaSettings": [{
        "schema": None, # projects/{project}/schemas/{schema}
        "encoding": None, # [JSON, BINARY, ENCODING_UNSPECIFIED]
    }],
    "labels": None,
}

subscription_properties = {
    "retainAckedMessages": None,
    "enableMessageOrdering": None,
    "retryPolicies": [{
        "minimumBackoff": None,
        "maximumBackoff": None,
    }],
    "pushConfigs": [{
        "host": None,
    }],
    "labels": None,
}
