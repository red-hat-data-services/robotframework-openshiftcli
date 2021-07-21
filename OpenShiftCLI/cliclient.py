from abc import ABC, abstractmethod


class Cliclient(ABC):

    @abstractmethod
    def apply(self, body, namespace):
        pass

    @abstractmethod
    def create(self, body, namespace):
        pass

    @abstractmethod
    def delete(self, name, namespace):
        pass

    @abstractmethod
    def get(self, name, namespace):
        pass
