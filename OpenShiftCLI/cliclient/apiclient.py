from typing import Any, Dict, Optional

from kubernetes import config
from openshift.dynamic import DynamicClient

from OpenShiftCLI.cliclient import CliClient


class ApiClient(CliClient):

    def __init__(self, api_version: str, kind: str) -> None:
        self.api_version = api_version
        self.client = DynamicClient(config.new_client_from_config())
        self.kind = kind

    def apply(self, body: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        return self._get_resources().apply(body=body, namespace=namespace).to_dict()

    def create(self, body: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        return self._get_resources().create(body=body, namespace=namespace).to_dict()

    def delete(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> Dict[str, Any]:
        return self._get_resources().delete(name=name, namespace=namespace, **kwargs).to_dict()

    def delete_from_file(self, body: str, namespace: Optional[str] = None, **kwargs: str) -> Dict[str, Any]:
        return self._get_resources().delete(body=body, namespace=namespace, **kwargs)

    def get(self,
            name: Optional[str] = None,
            namespace: Optional[str] = None,
            label_selector: Optional[str] = None) -> Dict[str, Any]:
        return self._get_resources().get(name=name, namespace=namespace, label_selector=label_selector).to_dict()

    def patch(self, name: str, body: str, namespace: Optional[str] = None, **kwargs: str) -> Dict[str, Any]:
        return self._get_resources().patch(name=name, body=body, namespace=namespace, **kwargs)

    def watch(self,
              namespace: Optional[str] = None,
              name: Optional[str] = None,
              timeout: Optional[int] = None) -> Dict[str, Any]:
        return self._get_resources().watch(namespace=namespace, name=name, timeout=timeout)

    def _get_resources(self) -> Any:
        return self.client.resources.get(api_version=self.api_version, kind=self.kind)
