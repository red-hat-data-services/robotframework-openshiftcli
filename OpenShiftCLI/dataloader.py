from abc import ABC, abstractmethod
from typing import Iterator


class DataLoader(ABC):

    @abstractmethod
    def load(self, path: str) -> Iterator:
        pass
