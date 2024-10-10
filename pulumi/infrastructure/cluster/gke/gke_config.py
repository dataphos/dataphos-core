cluster_properties = {
    "initialNodeCount": 3,
    "nodeConfigs": [{
        "machineType": "e2-medium",
        "oauthScopes": [
            "https://www.googleapis.com/auth/cloud-platform",
        ],
    }],
    "clusterAutoscalings": [{
        "autoscalingProfile": "BALANCED", # [BALANCED, OPTIMIZE_UTILIZATION]
        "enabled": False,
        "resourceLimits": [
          {
            "resource_type": "cpu",
            "minimum": 1,
            "maximum": 1,
          },
          {
            "resource_type": "memory",
            "minimum": 1,
            "maximum": 1,
          }
        ],
    }],
    "enableShieldedNodes": None,
    "binaryAuthorizations": [{
        "evaluationMode": None, # [DISABLED, PROJECT_SINGLETON_POLICY_ENFORCE]
    }],
    "verticalPodAutoscalings": [{
        "enabled": False,
    }],
    "resourceLabels": None,
}

kubeconfig_template = \
"""
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {0}
    server: https://{1}
  name: {2}
contexts:
- context:
    cluster: {2}
    user: {2}
  name: {2}
current-context: {2}
kind: Config
preferences: {{}}
users:
- name: {2}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: gke-gcloud-auth-plugin
      installHint: Install gke-gcloud-auth-plugin for use with kubectl by following
        https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
      provideClusterInfo: true
"""
