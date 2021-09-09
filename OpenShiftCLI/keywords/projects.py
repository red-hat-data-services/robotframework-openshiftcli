from typing import Optional

from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer
from OpenShiftCLI.errors import ResourceNotFound


class ProjectKeywords(LibraryComponent):
    def __init__(self,
                 cli_client: CliClient,
                 data_loader: DataLoader,
                 data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        LibraryComponent.__init__(self, cli_client, data_loader, data_parser, output_formatter, output_streamer)
        self.cli_client = cli_client
        self.data_loader = data_loader
        self.output_formatter = output_formatter
        self.output_streamer = output_streamer

    @keyword
    def delete_project(self, name: str, **kwargs: str) -> None:
        """Delete Project

        Args:
            name (str): Project to delete
        """
        self.process(operation="delete", type="name", name=name, **kwargs)

    @keyword
    def get_projects(self) -> None:
        """Get All Projects
        """
        self.process(operation="get", type="name")

    @keyword
    def new_project(self, name: str) -> None:
        """Create new Project

        Args:
            name (str): Project name
        """
        project = f"""
        apiVersion: project.openshift.io/v1
        kind: Project
        metadata:
          name: {name}
        spec:
          finalizers:
          - kubernetes
        """
        self.process(operation="create", type="body", data_type="yaml", body=project)

    @keyword
    def projects_should_contain(self, name: str) -> None:
        """Get projects containing name

        Args:
          name: String that must contain the name of the project
        """
        projects = self.cli_client.get()['items']
        result = [project for project in projects if name in project['metadata']['name']]
        if not result:
            error_message = f'Projects with name containing {name} not found'
            self.output_streamer.stream(error_message, "error")
            raise ResourceNotFound(error_message)
        output = [{project['metadata']['name']: project['status']['phase'] for project in result}]
        formatted_output = self.output_formatter.format(output, "Projects found")
        self.output_streamer.stream(formatted_output, "info")

    @keyword
    def wait_until_project_exists(self, name: Optional[str] = None, timeout: Optional[int] = 100) -> None:
        """Wait until a Project exists

        Args:
            name (Optional[str], optional): Project to wait for. Defaults to None.
            timeout (Optional[int], optional): Time to wait. Defaults to 100.
        """
        for event in self.cli_client.watch(namespace=None, name=None, timeout=timeout):
            if event['object']['metadata']['name'] == name:
                self.output_streamer.stream(f"Project {name} found", "info")
                self.output_streamer.stream(
                    f"{event['object']['metadata']['name']}\nStatus:{event['object']['status']['phase']}", "info")
                break

    @keyword
    def wait_until_project_does_not_exists(self, name: Optional[str] = None, timeout: Optional[int] = 100) -> None:
        """Wait until a Project doesn't exists

        Args:
            name (Optional[str], optional): Project to wait for. Defaults to None.
            timeout (Optional[int], optional): Time to wait. Defaults to 100.
        """
        for event in self.cli_client.watch(namespace=None, name=None, timeout=timeout):
            if event['object']['metadata']['name'] == name and event['type'] == "DELETED":
                self.output_streamer.stream(f"Project {name} Deleted", "info")
                break
