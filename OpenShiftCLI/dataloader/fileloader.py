from abc import ABC, abstractmethod


class FileLoader(ABC):

    @abstractmethod
    def from_file(self, path: str) -> str:
        pass
