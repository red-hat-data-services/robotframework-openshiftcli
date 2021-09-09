from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer


class ClusterroleKeywords(LibraryComponent):
    def __init__(self,
                 cli_client: CliClient,
                 data_loader: DataLoader,
                 data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        LibraryComponent.__init__(self, cli_client, data_loader, data_parser, output_formatter, output_streamer)

    @keyword
    def create_cluster_role(self, file: str) -> None:
        """Create Cluster Role

        Args:
            file (str): Path to the yaml file containing the Cluster Role definition
        """
        self.process(operation="create", type="body", data_type="yaml", file=file)

    @keyword
    def delete_cluster_role(self, name: str, **kwargs: str) -> None:
        """Delete Cluster Role

        Args:
            name (str): Cluster Role to delete
        """
        self.process(operation="delete", type="name", name=name, **kwargs)
