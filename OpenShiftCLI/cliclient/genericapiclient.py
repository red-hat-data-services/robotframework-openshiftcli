from typing import Any, Dict, List, Optional

from kubernetes import config
from openshift.dynamic import DynamicClient

from OpenShiftCLI.cliclient import GenericClient


class GenericApiClient(GenericClient):

    def __init__(self) -> None:
        self.dynamic_client = DynamicClient(config.new_client_from_config())

    def apply(self, kind: str, body: str, namespace: Optional[str] = None,
              **kwargs: str) -> Dict[str, Any]:
        return self._get_resources(kind=kind).apply(body=body, namespace=namespace,
                                                    **kwargs).to_dict()

    def create(self, kind: str, body: str, namespace: Optional[str] = None,
               **kwargs: str) -> Dict[str, Any]:
        return self._get_resources(kind=kind).create(body=body, namespace=namespace,
                                                     **kwargs).to_dict()

    def delete(self, kind: str, name: Optional[str] = None, namespace: Optional[str] = None,
               body: Optional[str] = None, label_selector: Optional[str] = None,
               field_selector: Optional[str] = None, **kwargs: str) -> Dict[str, Any]:
        return self._get_resources(kind=kind).delete(name=name, namespace=namespace, body=body,
                                                     label_selector=label_selector, field_selector=field_selector,
                                                     **kwargs).to_dict()

    def get(self, kind: str, name: Optional[str] = None, namespace: Optional[str] = None,
            label_selector: Optional[str] = None, field_selector: Optional[str] = None,
            **kwargs: str) -> Dict[str, Any]:
        return self._get_resources(kind=kind).get(name=name, namespace=namespace,
                                                  label_selector=label_selector,
                                                  field_selector=field_selector,
                                                  **kwargs).to_dict()

    def get_pod_logs(self, name: str, namespace: str, **kwargs: Optional[str]) -> Any:
        return self.dynamic_client.request('GET', f"/api/v1/namespaces/{namespace}/pods/{name}/log")

    def patch(self, kind: str, name: str, body: str, namespace: Optional[str] = None,
              **kwargs: str) -> Dict[str, Any]:
        return self._get_resources(kind=kind).patch(name=name, body=body, namespace=namespace,
                                                    **kwargs).to_dict()

    def watch(self, kind: str, namespace: Optional[str] = None, name: Optional[str] = None,
              label_selector: Optional[str] = None, field_selector: Optional[str] = None,
              resource_version: Optional[str] = None,
              timeout: Optional[int] = None) -> List[Dict[str, Any]]:
        events = self._get_resources(kind=kind).watch(namespace=namespace, name=name,
                                                      label_selector=label_selector,
                                                      field_selector=field_selector,
                                                      resource_version=resource_version,
                                                      timeout=timeout)
        return [{'type': event['type'], 'object': event['object'].to_dict()} for event in events]

    def _get_resources(self, kind: str) -> Any:
        return self.dynamic_client.resources.get(api_version=self._get_api_version(kind=kind),
                                                 kind=kind)

    def _get_api_version(self, kind: str) -> str:
        result = ""
        core = self.dynamic_client.request('GET', '/api/v1')
        if any(resource for resource in core.resources if resource.kind == kind):
            result = core.groupVersion
        else:
            groups = self.dynamic_client.request('GET', '/apis').groups
            for group in groups:
                api = self.dynamic_client.request('GET', f"/apis/{group.name}/{group.preferredVersion.version}")
                if any(resource for resource in api.resources if resource.kind == kind):
                    result = group.preferredVersion.groupVersion
                    break
        return result
