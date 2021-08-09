from abc import ABC, abstractmethod


class Cliclient(ABC):

    @abstractmethod
    def apply(self, body, namespace):
        pass

    @abstractmethod
    def create(self, body, namespace):
        pass

    @abstractmethod
    def delete(self, name, namespace, **kwargs):
        pass

    @abstractmethod
    def delete_from_file(self, body, namespace, **kwargs):
        pass

    @abstractmethod
    def get(self, name, namespace):
        pass

    @abstractmethod
    def patch(self, name, body, namespace, **kwargs):
        pass

    @abstractmethod
    def watch(self, namespace, name, timeout):
        pass
