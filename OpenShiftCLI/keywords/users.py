from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer


class UserKeywords(LibraryComponent):
    def __init__(self,
                 cli_client: CliClient,
                 data_loader: DataLoader,
                 data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        LibraryComponent.__init__(self, cli_client, data_loader, data_parser, output_formatter, output_streamer)

    @keyword
    def create_user(self, file: str) -> None:
        """Create User

        Args:
            file (str): Path to the yaml file containing the User definition
        """
        self.process(operation="create", type="body", data_type="yaml", file=file)

    @keyword
    def delete_user(self, name: str, **kwargs: str) -> None:
        """Delete User

        Args:
            name (str): User to delete
        """
        self.process(operation="delete", type="name", name=name, **kwargs)
