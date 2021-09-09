from typing import Optional

from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer


class RoleKeywords(LibraryComponent):
    def __init__(self, cli_client: CliClient,
                 data_loader: DataLoader, data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        LibraryComponent.__init__(self, cli_client, data_loader, data_parser, output_formatter, output_streamer)

    @keyword
    def create_role(self, file: str, namespace: Optional[str] = None) -> None:
        """Create Role

        Args:
            file (str): Path to the yaml file containing the Role definition
            namespace (Optional[str]): Namespace where the Role will be created
        """
        self.process(operation="create", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    def delete_role(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Role

        Args:
            name (str): Role to delete
            namespace (Optional[str]): Namespace where the Role exists
        """
        self.process(operation="delete", type="name", name=name, namespace=namespace, **kwargs)
