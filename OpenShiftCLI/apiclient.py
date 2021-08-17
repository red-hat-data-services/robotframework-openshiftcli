from OpenShiftCLI.cliclient import Cliclient
from kubernetes import config
from openshift.dynamic import DynamicClient


class Apiclient(Cliclient):

    def __init__(self, api_version, kind) -> None:
        self.api_version = api_version
        self.dynamic_client = DynamicClient(config.new_client_from_config())
        self.kind = kind

    def apply(self, body, namespace):
        return self._get_objects().apply(body=body, namespace=namespace)

    def create(self, body, namespace):
        return self._get_objects().create(body=body, namespace=namespace)

    def delete(self, name, namespace, **kwargs):
        return self._get_objects().delete(name=name, namespace=namespace, **kwargs)

    def delete_from_file(self, body, namespace, **kwargs):
        return self._get_objects().delete(body=body, namespace=namespace, **kwargs)

    def get(self, name, namespace, label_selector):
        return self._get_objects().get(name=name, namespace=namespace, label_selector=label_selector)

    def patch(self, name, body, namespace, **kwargs):
        return self._get_objects().patch(name=name, body=body, namespace=namespace, **kwargs)

    def watch(self, namespace, name, timeout):
        return self._get_objects().watch(namespace=namespace, name=name, timeout=timeout)

    def _get_objects(self):
        return self.dynamic_client.resources.get(api_version=self.api_version, kind=self.kind)
