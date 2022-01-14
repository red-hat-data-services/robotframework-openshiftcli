from abc import ABC, abstractmethod


class Jinja2Loader(ABC):

    @abstractmethod
    def from_jinja2(self, src: str, variables: str) -> str:
        pass
