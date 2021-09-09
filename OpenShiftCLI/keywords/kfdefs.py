from typing import Optional

from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer


class KFDEFKeywords(LibraryComponent):
    def __init__(self,
                 cli_client: CliClient,
                 data_loader: DataLoader,
                 data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        LibraryComponent.__init__(self, cli_client, data_loader, data_parser, output_formatter, output_streamer)
        self.cli_client = cli_client
        self.output_formatter = output_formatter
        self.output_streamer = output_streamer

    @keyword
    def create_kfdef(self, file: str, namespace: Optional[str] = None) -> None:
        """Create KfDef

        Args:
            file(str): Path to the yaml file containing the KfDef definition
            namespace (Optional[str]): Namespace where the KfDef will be created
        """
        self.process(operation="create", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    def delete_kfdef(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete KfDef

        Args:
            name (str): KfDef to delete
            namespace (Union[str, None], optional): Namespace where the KfDef exists. Defaults to None.
        """
        self.process(operation="delete", type="name", name=name, namespace=namespace, **kwargs)

    @keyword
    def get_kfdefs(self, namespace: Optional[str] = None, label_selector: Optional[str] = None) -> None:
        """Get KfDefs

        Args:
            namespace (Optional[str], optional): Namespace where the KfDefs exist. Defaults to None.
            label_selector (Optional[str], optional): Label selector of the KfDefs. Defaults to None.
        """
        self.process(operation="get", type="name", namespace=namespace, label_selector=label_selector)

    @keyword
    def patch_kfdef(self,
                    name: Optional[str] = None,
                    body: Optional[str] = None,
                    namespace: Optional[str] = None,
                    **kwargs: str) -> None:
        """Patch KfDef

        Args:
            name (Optional[str], optional): KfDef to patch. Defaults to None.
            body (Optional[str], optional): KfDef definition file. Defaults to None.
            namespace (Optional[str], optional): Namespace where the KfDef exists. Defaults to None.
        """
        self.process(operation="patch", type="patch", data_type="json",
                     name=name, body=body, namespace=namespace, **kwargs)
