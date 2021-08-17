from typing import Optional

from robotlibcore import keyword

from OpenShiftCLI.cliclient import Cliclient
from OpenShiftCLI.logstreamer import LogStreamer
from OpenShiftCLI.yamlloader import YamlLoader


class SecretKeywords(object):
    def __init__(self, cliclient: Cliclient, dataloader: YamlLoader, outputstreamer: LogStreamer) -> None:
        self.cliclient = cliclient
        self.dataloader = dataloader
        self.outputstreamer = outputstreamer

    @keyword
    def apply_secret(self, filename: str, namespace: Optional[str] = None) -> None:
        """Apply Secret

        Args:
            filename (str): Path to the yaml file containing the Secret definition
            namespace (Optional[str], optional): Namespace where the Secret exists. Defaults to None.
        """
        data = self.dataloader.load(filename)
        for secret_data in data:
            result = self.cliclient.apply(body=secret_data, namespace=namespace)
            self.outputstreamer.stream(result, "info")

    @keyword
    def create_secret(self, filename: str, namespace: Optional[str] = None) -> None:
        """Create Secret

        Args:
            filename (str): Path to the yaml file containing the Secret definition
            namespace (Optional[str]): Namespace where the Secret will be created
        """
        data = self.dataloader.load(filename)
        for secret_data in data:
            result = self.cliclient.create(body=secret_data, namespace=namespace)
            self.outputstreamer.stream(result, "info")

    @keyword
    def delete_secret(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Secret

        Args:
            name (str): Secret to delete
            namespace (Optional[str], optional): Namespace where the Secret exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        self.outputstreamer.stream(result, "info")

    @keyword
    def delete_secret_from_file(self, filename: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Secret From File

        Args:
            filename (str): Path to the yaml file containing the Secret definition
            namespace (Optional[str], optional): Namespace where the Secret exists. Defaults to None.
        """
        data = self.dataloader.load(filename)
        for secret_data in data:
            result = self.cliclient.delete(name=secret_data['metadata']['name'],
                                           namespace=namespace or secret_data['metadata']['namespace'], **kwargs)
            self.outputstreamer.stream(result, "info")
