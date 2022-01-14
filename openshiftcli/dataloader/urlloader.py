from abc import ABC, abstractmethod


class UrlLoader(ABC):

    @abstractmethod
    def from_url(self, path: str) -> str:
        pass
