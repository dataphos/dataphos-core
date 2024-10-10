from abc import ABC, abstractmethod

from infrastructure.ResourceCreator import ResourceCreator


class AbstractKubernetesCluster(ABC, ResourceCreator):

    @abstractmethod
    def get_kubernetes_provider(self):
        raise NotImplementedError
