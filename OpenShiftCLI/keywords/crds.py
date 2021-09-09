from typing import Optional

from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer


class CRDKeywords(LibraryComponent):
    def __init__(self,
                 cli_client: CliClient,
                 data_loader: DataLoader,
                 data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        LibraryComponent.__init__(self, cli_client, data_loader, data_parser, output_formatter, output_streamer)

    @keyword
    def create_crd(self, file: str, namespace: Optional[str] = None) -> None:
        """Create Custom Resource Definition

        Args:
            file (str): Path to the yaml file containing the Custom Resource Definition definition
            namespace (Optional[str]): Namespace where the Custom Resource Definition will be created. Defaults to None.
        """
        self.process(operation="create", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    def delete_crd(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Custom Resource Definition

        Args:
            name (str): Custom Resource Definition to delete
            namespace (Optional[str], optional): Namespace where the CRD exists. Defaults to None.
        """
        self.process(operation="delete", type="name", name=name, namespace=namespace, **kwargs)
