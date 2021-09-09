import time

from typing import Optional
from typing_extensions import Literal

from robotlibcore import keyword
from robot.api import Error

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer


class PodKeywords(LibraryComponent):
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
    def create_pod(self, file: str, namespace: Optional[str] = None) -> None:
        """Create Pod

        Args:
            file (str): Path to the yaml file containing the Pod definition
            namespace (Optional[str], optional): Namespace where Pod will be created. Defaults to None.
        """
        self.process(operation="create", type="body", data_type="yaml", file=file, namespace=namespace)

    @keyword
    def delete_pod(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Pod

        Args:
            name (str): Pod to delete
            namespace (Optional[str]): Namespace where the Pod exists
        """
        self.process(operation="delete", type="name", name=name, namespace=namespace, **kwargs)

    @keyword
    def get_pods(self, namespace: Optional[str] = None, label_selector: Optional[str] = None, **kwargs: str) -> None:
        """Get Pods

        Args:
            namespace (Optional[str], optional): Namespace to list Pods from. Defaults to None.
            label_selector (Optional[str], optional): Label selector of the Pods. Defaults to None.
        """
        self.process(operation="get", type="name", namespace=namespace, label_selector=label_selector, **kwargs)

    @keyword
    def search_pods(self, name: str = "",
                    label_selector: Optional[str] = None,
                    namespace: Optional[str] = None) -> None:
        """Search for pods with name containing a given string and/or
           having a given label selector and/or from a given namespace

        Args:
            name (Optional[str], optional): String that pods name should contain. Defaults to None.
            label_selector (Optional[str], optional): Label selector that pods should have. Defaults to None.
            namespace (Optional[str], optional): [description]. Defaults to None.
        """
        pods = self.cli_client.get(namespace=namespace, label_selector=label_selector)['items']
        result = [pod for pod in pods if name in pod['metadata']['name']]
        if not result:
            self.output_streamer.stream('Pods not found in search', "error")
            raise Error('Pods not found in search')
        self.output_streamer.stream(self.output_formatter.format(result, "Pods found", "status"), "info")

    @keyword
    def wait_for_pods_number(self, number: int,
                             namespace: Optional[str] = None,
                             label_selector: Optional[str] = None,
                             timeout: int = 60,
                             comparison: Literal["EQUAL", "GREATER THAN", "LESS THAN"] = "EQUAL") -> None:
        """Wait for a given number of pods to exist

        Args:
            number (int): Number of pods to wait for
            namespace (Optinal[str], optional): Namespace where the pods exist. Defaults to None.
            label_selector (Optional[str], optional): Label selector of the pods. Defaults to None.
            timeout (int, optional): Time to wait for the pods. Defaults to 60.
            comparison (Literal[, optional): Comparison between expected and actual number of pods. Defaults to "EQUAL".
        """
        max_time = time.time() + timeout
        while time.time() < max_time:
            pods_number = len(self.cli_client.get(namespace=namespace, label_selector=label_selector)['items'])
            if pods_number == number and comparison == "EQUAL":
                self.output_streamer.stream(f"Pods number: {number} succeeded", "info")
                break
            elif pods_number > number and comparison == "GREATER THAN":
                self.output_streamer.stream(f"Pods number greater than: {number} succeeded", "info")
                break
            elif pods_number < number and comparison == "LESS THAN":
                self.output_streamer.stream(f"Pods number less than: {number} succeeded", "info")
                break
        else:
            pods = self.cli_client.get(namespace=namespace, label_selector=label_selector)['items']
            pods_number = len(pods)
            self.output_streamer.stream(self.output_formatter.format(
                pods, f"Timeout - {pods_number} pods found", "name"), "warn")

    @keyword
    def wait_for_pods_status(self, namespace: Optional[str] = None,
                             label_selector: Optional[str] = None,
                             timeout: int = 60) -> None:
        """Wait for pods status

        Args:
            namespace (Optional[str, None], optional): Namespace where the pods exist. Defaults to None.
            label_selector (Optional[str], optional): Pods' label selector. Defaults to None.
            timeout (int, optional): Time to wait for pods status. Defaults to 60.
        """
        max_time = time.time() + timeout
        failing_containers = []
        while time.time() < max_time:
            pods = self.cli_client.get(namespace=namespace, label_selector=label_selector)['items']
            if pods:
                pending_pods = [pod for pod in pods if pod['status']['phase'] == "Pending"]
                if not pending_pods:
                    failing_pods = [pod for pod in pods if pod['status']['phase']
                                    == "Failed" or pod['status']['phase'] == "Unknown"]
                    if failing_pods:
                        self.output_streamer.stream(self.output_formatter.format(
                            failing_pods, "Error in Pod", "wide"), "error")
                        raise Error(self.output_formatter.format(
                            failing_pods, "There are pods in status Failed or Unknown: ", "name"))

                    failing_containers = [pod for pod in pods if pod['status']['phase']
                                          == "Running" and pod['status']['conditions'][1]['status'] != "True"]

                    if not failing_containers:
                        self.output_streamer.stream(self.output_formatter.format(pods, "Pods", "wide"), "info")
                        break
        else:
            self.output_streamer.stream(self.output_formatter.format(
                failing_containers, "Timeout - Pods with containers not ready", "wide"), "warn")
