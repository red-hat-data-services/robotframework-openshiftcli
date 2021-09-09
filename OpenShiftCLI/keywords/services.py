from typing import Optional

from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer
from OpenShiftCLI.errors import ResourceNotFound


class ServiceKeywords(LibraryComponent):
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
    def create_service(self, file: str, namespace: Optional[str] = None) -> None:
        """Create Service

        Args:
            file(str): Path to the yaml file containing the Service definition
            namespace (Optional[str]): Namespace where the Cluster Service will be created
        """
        self.process(operation="create", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    def get_services(self, namespace: Optional[str] = None) -> None:
        """Get all services

        Args:
            namespace (str, optional): Namespace. Defaults to None.
        """
        self.process(operation="get", type="name", namespace=namespace)

    @keyword
    def delete_service(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Service

        Args:
            name (str): Service to delete
            namespace (Optional[str], optional): Namespace where the Service exists. Defaults to None.
        """
        self.process(operation="delete", type="name", name=name, namespace=namespace, **kwargs)

    @keyword
    def services_should_contain(self, name: str, namespace: Optional[str] = None) -> None:
        """
        Get services containing name

        Args:
          name: String that must contain the name of the service
          namespace (Optional[str], optional): Namespace where the Service exists. Defaults to None.
        """
        services = self.cli_client.get(namespace=namespace)['items']
        result = [service for service in services if name in service['metadata']['name']]
        if not result:
            error_message = f"Services with name containing {name} not found"
            self.output_streamer.stream(error_message, 'error')
            raise ResourceNotFound(error_message)
        output = [{service['metadata']['name']: f"{service['spec']['clusterIPs']}:{service['spec']['ports']}"}
                  for service in result]
        formatted_output = self.output_formatter.format(output, "Services found")
        self.output_streamer.stream(formatted_output, "info")
