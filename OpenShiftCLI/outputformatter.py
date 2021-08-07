from abc import ABC, abstractmethod
from typing import List


class OutputFormatter(ABC):

    @abstractmethod
    def format(self, message: str, objects: List, type: str) -> str:
        pass
