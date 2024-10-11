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
