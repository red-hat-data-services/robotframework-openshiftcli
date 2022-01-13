from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class GenericClient(ABC):

    @abstractmethod
    def apply(self, kind: str, body: str, namespace: Optional[str] = None,
              **kwargs: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create(self, kind: str, body: str, namespace: Optional[str] = None,
               **kwargs: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete(self, kind: str, name: Optional[str] = None, namespace: Optional[str] = None,
               body: Optional[str] = None, label_selector: Optional[str] = None,
               field_selector: Optional[str] = None, **kwargs: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get(self, kind: str, name: Optional[str] = None, namespace: Optional[str] = None,
            label_selector: Optional[str] = None, field_selector: Optional[str] = None,
            **kwargs: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_pod_logs(self, name: str, namespace: str, **kwargs: Optional[str]) -> Any:
        pass

    @abstractmethod
    def patch(self, kind: str, name: str, body: str, namespace: Optional[str] = None,
              **kwargs: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def watch(self, kind: str, namespace: Optional[str] = None, name: Optional[str] = None,
              label_selector: Optional[str] = None, field_selector: Optional[str] = None,
              resource_version: Optional[str] = None, timeout: Optional[int] = None) -> List[Dict[str, Any]]:
        pass
