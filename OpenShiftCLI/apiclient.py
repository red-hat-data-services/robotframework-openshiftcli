from OpenShiftCLI.cliclient import Cliclient
from kubernetes import config
from openshift.dynamic import DynamicClient


class Apiclient(Cliclient):

    def __init__(self, api_version, kind) -> None:
        self.k8s_client = config.new_client_from_config()
        self.dyn_client = DynamicClient(self.k8s_client)
        self.objects = self.dyn_client.resources.get(api_version=api_version, kind=kind)

    def apply(self, body, namespace):
        return self.objects.apply(body=body, namespace=namespace)

    def create(self, body, namespace):
        return self.objects.create(body=body, namespace=namespace)

    def delete(self, name, namespace):
        return self.objects.delete(name=name, namespace=namespace)

    def get(self, name, namespace):
        return self.objects.get(name=name, namespace=namespace)
