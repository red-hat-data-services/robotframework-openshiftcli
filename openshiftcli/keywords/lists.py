from typing import Optional

from robotlibcore import keyword

from openshiftcli.base import LibraryComponent
from openshiftcli.cliclient import CliClient
from openshiftcli.dataloader import DataLoader
from openshiftcli.dataparser import DataParser
from openshiftcli.deprecated import deprecated
from openshiftcli.outputformatter import OutputFormatter
from openshiftcli.outputstreamer import OutputStreamer


class ListKeywords(LibraryComponent):
    def __init__(self,
                 cli_client: CliClient,
                 data_loader: DataLoader,
                 data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        LibraryComponent.__init__(self, cli_client, data_loader, data_parser, output_formatter, output_streamer)

    @keyword
    @deprecated(new_keyword='Apply')
    def apply_resources_list(self, file: str, namespace: Optional[str] = None) -> None:
        """Apply Resources List

        Args:
            file (str): Path to the yaml file containing the Resources List definition
            namespace (str, optional): Namespace where the Resources List will be created. Defaults to None.
        """
        self.process(operation="apply", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    @deprecated(new_keyword='Create')
    def create_resources_list(self, file: str, namespace: Optional[str] = None) -> None:
        """Create Resources List

        Args:
            file (str): Path to yaml file containing the Resources List definition
            namespace (Optional[str], optional): Namespace where the Resources List will be created
        """
        self.process(operation="create", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    @deprecated(new_keyword='Delete')
    def delete_resources_list(self, file: str, namespace: Optional[str] = None) -> None:
        """Delete Resources List

        Args:
            file (str): Path to the Resources List to delete
            namespace (Union[str, None], optional): Namespace where the Resources List exists. Defaults to None.
        """
        self.process(operation="delete_from_file", type="body", data_type="yaml", file=file, namespace=namespace)
