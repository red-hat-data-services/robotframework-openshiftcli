import os
from robotlibcore import keyword
from robot.api import Error
from typing import List, Dict, Optional, Union
import time

import yaml
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class PodKeywords(object):
    def __init__(self, cliclient, output_formatter, output_streamer) -> None:
        self.cliclient = cliclient
        self.output_formatter = output_formatter
        self.output_streamer = output_streamer

    @keyword
    def create_pod(self, filename: str, namespace: Optional[str] = None) -> None:
        """Create Pod

        Args:
            filename (str): Path to the yaml file containing the Pod definition
            namespace (Optional[str]): Namespace where Pod will be created
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            pod_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=pod_data, namespace=namespace)
        self.output_streamer.stream(result, "info")

    @keyword
    def delete_pod(self, name: str, namespace: Optional[str] = None, **kwargs: str) -> None:
        """Delete Pod

        Args:
            name (str): Pod to delete
            namespace (Optional[str]): Namespace where the Pod exists
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        self.output_streamer.stream(result, "info")

    @keyword
    def get_pods(self, namespace: Union[str, None] = None, label_selector: Union[str, None] = None, **kwargs) -> List:
        """Get Pods

        Args:
            namespace (Union[str, None], optional): Namespace to list pods from. Defaults to None.

        Raises:
            Error: Raises error if not pods found

        Returns:
            List: List of pods
        """

        result = self.cliclient.get(name=None, namespace=namespace, label_selector=label_selector, **kwargs).items
        if not result:
            self.output_streamer.stream(f'Pods not found in {namespace}', "error")
            raise Error(f'Pods not found in {namespace}')
        return result

    @keyword
    def search_pods(self, name: str = "",
                    label_selector: Optional[str] = None,
                    namespace: Optional[str] = None) -> List[Dict[str, str]]:
        """Search for pods with name containing a given string and/or
           having a given label selector and/or from a given namespace

        Args:
            name (Optional[str], optional): String that pods name should contain. Defaults to None.
            label_selector (Optional[str], optional): Label selector that pods should have. Defaults to None.
            namespace (Optional[str], optional): [description]. Defaults to None.

        Raises:
            Error: Raise error if not pods found in search

        Returns:
            List[Dict[str, str]]: List of pods found in search
        """
        pods = self.cliclient.get(name=None, namespace=namespace, label_selector=label_selector).items

        result = [pod for pod in pods if name in pod.metadata.name]
        if not result:
            self.output_streamer.stream('Pods not found in search', "error")
            raise Error('Pods not found in search')
        self.output_streamer.stream(self.output_formatter.format("Pods found", result, "status"), "info")
        return result

    @keyword
    def wait_for_pods_number(self, number: int,
                             namespace: Union[str, None] = None,
                             label_selector: Union[str, None] = None,
                             timeout: int = 60,
                             comparison: Literal["EQUAL", "GREATER THAN", "LESS THAN"] = "EQUAL") -> None:
        """Wait for a given number of pods to exist

        Args:
            number (int): Number of pods to wait for
            namespace (Union[str, None], optional): Namespace where the pods exist. Defaults to None.
            label_selector (Union[str, None], optional): Label selector of the pods. Defaults to None.
            timeout (Union[int, None], optional): Time to wait for the pods. Defaults to 60.
            comparison (Literal[, optional): Comparison between expected and actual number of pods. Defaults to "EQUAL".
        """
        max_time = time.time() + timeout
        while time.time() < max_time:
            pods_number = len(self.get_pods(namespace=namespace, label_selector=label_selector))
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
            pods_number = len(self.get_pods(namespace=namespace, label_selector=label_selector))
            self.output_streamer.stream(f"Timeout - {pods_number} found pods:", "warn")

    @keyword
    def wait_for_pods_status(self, namespace: Union[str, None] = None,
                             label_selector: Union[str, None] = None,
                             timeout: int = 60) -> None:
        """Wait for pods status

        Args:
            namespace (Union[str, None], optional): Namespace where the pods exist. Defaults to None.
            label_selector (Union[str, None], optional): Pods' label selector. Defaults to None.
            timeout (int, optional): Time to wait for pods status. Defaults to 60.

        Raises:
            Error: Raises error if there are pods in status failed or unknown
        """
        max_time = time.time() + timeout
        while time.time() < max_time:
            pods = self.get_pods(namespace=namespace, label_selector=label_selector)
            if pods:
                pending_pods = [pod for pod in pods if pod.status.phase == "Pending"]
                if not pending_pods:
                    failing_pods = [pod for pod in pods if pod.status.phase
                                    == "Failed" or pod.status.phase == "Unknown"]
                    if failing_pods:
                        self.output_streamer.stream(self.output_formatter.format(
                            "Error in Pod", failing_pods, "wide"), "error")
                        raise Error(self.output_formatter.format(
                            "There are pods in status Failed or Unknown: ", failing_pods, "name"))

                    failing_containers = [pod for pod in pods if pod.status.phase
                                          == "Running" and pod.status.conditions[3].status != "True"]
                    if not failing_containers:
                        self.output_streamer.stream(self.output_formatter.format("Pod", pods, "wide"), "info")
                        break
        else:
            self.output_streamer.stream(self.output_formatter.format(
                "Timeout - Pods:", self.get_pods(namespace), "wide"), "warn")
