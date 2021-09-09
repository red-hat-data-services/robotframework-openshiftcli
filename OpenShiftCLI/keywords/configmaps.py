from typing import Optional

from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer


class ConfigmapKeywords(LibraryComponent):
    def __init__(self,
                 cli_client: CliClient,
                 data_loader: DataLoader,
                 data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        LibraryComponent.__init__(self, cli_client, data_loader, data_parser, output_formatter, output_streamer)

    @keyword
    def create_configmap(self, file: str, namespace: Optional[str] = None) -> None:
        """Create Configmap

        Args:
            file (str): Path to the yaml file containing the Configmap definition
            namespace (Optional[str], optional): Namespace where the Configmap will be created. Defaults to None.
        """
        self.process(operation="create", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    def delete_configmap(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete ConfigMap

        Args:
            name (str): ConfigMap to delete
            namespace (Optional[str], optional): Namespace where the ConfigMap exists. Defaults to None.
        """
        self.process(operation="delete", type="name", name=name, namespace=namespace, **kwargs)

    @keyword
    def delete_configmap_from_file(self, file: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Configmap From File

        Args:
            file (str): Path to the yaml file containing the Configmap definition
            namespace (Optional[str], optional): Namespace where the Configmap exists. Defaults to None.
        """
        self.process(operation="delete", type="name", data_type="yaml", file=file, namespace=namespace, **kwargs)

    @keyword
    def patch_configmap(self,
                        name: Optional[str] = None,
                        body: Optional[str] = None,
                        namespace: Optional[str] = None,
                        **kwargs: str) -> None:
        """Patch Configmap

        Args:
            name (Optional[str], optional): Configmap to patch. Defaults to None.
            body (Optional[str], optional): Configmap definition file. Defaults to None.
            namespace (Optional[str], optional): Namespace where the Configmap exists. Defaults to None.
        """
        self.process(operation="patch", type="patch", data_type="json",
                     name=name, body=body, namespace=namespace, **kwargs)
