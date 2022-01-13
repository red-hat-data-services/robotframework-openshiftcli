from abc import ABC, abstractmethod
from typing import Any, Dict, List


class YamlParser(ABC):

    @abstractmethod
    def from_yaml(self, data: str) -> List[Dict[str, Any]]:
        pass
