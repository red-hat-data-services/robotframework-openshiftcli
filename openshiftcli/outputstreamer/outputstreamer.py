from abc import ABC, abstractmethod


class OutputStreamer(ABC):

    @abstractmethod
    def stream(self, output: str, type: str) -> None:
        pass
