from typing import Optional

from robotlibcore import keyword

from OpenShiftCLI.base import LibraryComponent
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer
import datetime


class EventKeywords(LibraryComponent):
    def __init__(
        self,
        cli_client: CliClient,
        data_loader: DataLoader,
        data_parser: DataParser,
        output_formatter: OutputFormatter,
        output_streamer: OutputStreamer,
    ) -> None:
        LibraryComponent.__init__(
            self,
            cli_client,
            data_loader,
            data_parser,
            output_formatter,
            output_streamer,
        )

    @keyword
    def get_events(self,
                   name: Optional[str] = None,
                   namespace: Optional[str] = None,
                   label_selector: Optional[str] = None,
                   field_selector: Optional[str] = None,
                   **kwargs: str) -> None:
        """Get all events

        Args:
            namespace (str, optional): Namespace. Defaults to None.
        """
        result = self.cli_client.get(
            name=name,
            namespace=namespace,
            label_selector=label_selector,
            field_selector=field_selector,
            ** kwargs)["items"]
        output = [
            f'Time: {datetime.datetime.strptime(item["metadata"]["creationTimestamp"], "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y %H:%M:%S")}\n'
            f'Reason: {item["reason"]}\n'
            f'Component: {item["source"]["component"]}\n'
            f'Host: {item["source"]["host"]}\n'
            f'Resource: {item["involvedObject"]["kind"]}/{item["metadata"]["name"]}\n'
            f'Type: {item["type"]}\n'
            f'Message: {item["message"]}\n'
            for item in result
        ]
        self.output_streamer.stream(
            self.output_formatter.format(output, "Events"), "info"
        )
