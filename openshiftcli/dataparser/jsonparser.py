from abc import ABC, abstractmethod
from typing import Any, Dict, List


class JsonParser(ABC):

    @abstractmethod
    def from_json(self, data: str) -> List[Dict[str, Any]]:
        pass
