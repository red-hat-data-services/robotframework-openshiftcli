from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class CliClient(ABC):

    @abstractmethod
    def apply(self, body: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create(self, body: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_from_file(self, body: str, namespace: Optional[str] = None, **kwargs: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get(self,
            name: Optional[str] = None,
            namespace: Optional[str] = None,
            label_selector: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def patch(self, name: str, body: str, namespace: Optional[str] = None, **kwargs: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def watch(self,
              namespace: Optional[str] = None,
              name: Optional[str] = None,
              timeout: Optional[int] = None) -> Dict[str, Any]:
        pass
