from OpenShiftCLI.cliclient import Cliclient
from kubernetes import config
from openshift.dynamic import DynamicClient


class Apiclient(Cliclient):

    def __init__(self, api_version, kind) -> None:
        self.k8s_client = config.new_client_from_config()
        self.dyn_client = DynamicClient(self.k8s_client)
        self.objects = self.dyn_client.resources.get(api_version=api_version, kind=kind)

    def apply(self, body):
        return self.objects.apply(body=body)

    def create(self, body):
        return self.objects.create(body=body)

    def delete(self, body):
        return self.objects.delete(body)

    def get(self, name=None, namespace=None):
        return self.objects.get(name=name, namespace=namespace)
