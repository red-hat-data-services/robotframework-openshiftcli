from typing import Optional

from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer


class SecretKeywords(LibraryComponent):
    def __init__(self,
                 cli_client: CliClient,
                 data_loader: DataLoader,
                 data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        LibraryComponent.__init__(self, cli_client, data_loader, data_parser, output_formatter, output_streamer)

    @keyword
    def apply_secret(self, file: str, namespace: Optional[str] = None) -> None:
        """Apply Secret

        Args:
            file (str): Path to the yaml file containing the Secret definition
            namespace (Optional[str], optional): Namespace where the Secret exists. Defaults to None.
        """
        self.process(operation="apply", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    def create_secret(self, file: str, namespace: Optional[str] = None) -> None:
        """Create Secret

        Args:
            file (str): Path to the yaml file containing the Secret definition
            namespace (Optional[str], optional): Namespace where the Secret will be created
        """
        self.process(operation="create", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    def delete_secret(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Secret

        Args:
            name (str): Secret to delete
            namespace (Optional[str], optional): Namespace where the Secret exists. Defaults to None.
        """
        self.process(operation="delete", type="name", name=name, namespace=namespace, **kwargs)

    @keyword
    def delete_secret_from_file(self, file: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Secret From File

        Args:
            file (str): Path to the yaml file containing the Secret definition
            namespace (Optional[str], optional): Namespace where the Secret exists. Defaults to None.
        """
        self.process(operation="delete", type="name", data_type="yaml", file=file, namespace=namespace, **kwargs)
