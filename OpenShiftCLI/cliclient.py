from abc import ABC, abstractmethod


class Cliclient(ABC):

    @abstractmethod
    def apply(self, body):
        pass

    @abstractmethod
    def create(self, body):
        pass

    @abstractmethod
    def delete(self, body):
        pass

    @abstractmethod
    def get(self, name, namespace):
        pass
