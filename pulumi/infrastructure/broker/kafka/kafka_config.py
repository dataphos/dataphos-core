cluster_properties = {
    "strimziOperatorNamespace": "strimzi-operator",
    "clusterNamespace": "kafka-cluster",
    "clusterName": "kafka-cluster",
    "listeners": [
        {
            # plain
            "name": "clients",
            "port": 9092,
            "type": "internal",
            "tls": False,
        },
        {
            # tls
            "name": "clientstls",
            "port": 9093,
            "type": "internal",
            "tls": True,
        },
        {
            # external
            "name": "external",
            "port": 9094,
            "type": "loadbalancer",
            "tls": False,
        },
    ],
}

topic_properties = {
    "partitions": 3,
    "replicas": 1,
    "config": {
        "retentionMs": None,
        "segmentBytes": None,
    },
}
