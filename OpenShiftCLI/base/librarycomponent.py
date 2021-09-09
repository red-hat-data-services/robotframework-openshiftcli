import os
import validators

from typing import Any, Dict, List, Optional, Union
#
from OpenShiftCLI.cliclient import CliClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer
from OpenShiftCLI.errors import ResourceNotFound, ResourceOperationFailed


class LibraryComponent(object):
    def __init__(self,
                 cli_client: CliClient,
                 data_loader: DataLoader,
                 data_parser: DataParser,
                 output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer) -> None:
        self.cli_client = cli_client
        self.data_loader = data_loader
        self.data_parser = data_parser
        self.output_formatter = output_formatter
        self.output_streamer = output_streamer
        self.arguments : Dict[str, Optional[str]] = {}

    def process(self, operation: str, type: str, data_type: Optional[str] = None, **kwargs: Optional[str]) -> None:
        self.arguments = kwargs.copy()
        src = self._get_data_src()
        data = self._load_data(src)
        items = self._parse_data(data, data_type)
        self._process(items, operation, type)

    def _get_data_src(self) -> str:
        src = ""
        if "file" in self.arguments:
            src = self.arguments.pop("file")
        elif "body" in self.arguments:
            src = self.arguments.get("body")
        return src

    def _load_data(self, src: str) -> str:
        data = ""
        if validators.url(src):
            data = self.data_loader.from_url(src)
        elif os.path.isfile(src):
            data = self.data_loader.from_file(src)
        else:
            data = src
        return data

    def _parse_data(self, data: str, data_type: Optional[str]) -> List[Dict[str, Any]]:
        items = None
        if data_type == "yaml":
            items = self.data_parser.from_yaml(data)
        elif data_type == "json":
            items = self.data_parser.from_json(data)
        else:
            items = [{'item': {}}]
        return items

    def _config_arguments(self, item: Union[str, Dict[str, Any]], type: str) -> None:
        if type == "patch":
            self.arguments["body"] = item
            self.arguments["content_type"] = "application/merge-patch+json"
        elif type == "body":
            self.arguments["body"] = item
        elif type == "name":
            self.arguments["name"] = item['metadata']['name'] \
                if 'metadata' in item and 'name' in item['metadata'] \
                else self.arguments.get("name")
            self.arguments["namespace"] = item['metadata']['namespace'] \
                if 'metadata' in item and 'namespace' in item['metadata'] \
                else self.arguments.get(
                "namespace")

    def _process_one(self, operation: str,) -> Dict[str, Any]:
        result = None
        try:
            result = getattr(self.cli_client, operation)(**self.arguments)
        except AttributeError as error:
            error_message = f"Operation {operation} does not exists:\n{error}"
            self.output_streamer.stream(error_message, "error")
            raise ResourceOperationFailed(error_message)
        except Exception as error:
            error_message = f"{operation.capitalize()} failed:\n{error}"
            self.output_streamer.stream(error_message, "error")
            raise ResourceOperationFailed(error_message)
        return result

    def _generate_output(self,
                         output: Union[Dict[str, Any], List[Dict[str, Any]]],
                         message: str,
                         type: Optional[str] = None) -> None:
        self.output_streamer.stream(self.output_formatter.format(output, message, type), "info")

    def _process(self, items: List[Dict[str, Any]], operation: str, type: str):
        for item in items:
            self._config_arguments(item, type)
            result = self._process_one(operation)
            kind = result['kind']
            output_message = f"{operation.capitalize()} result"
            output_type = None
            if type == "name" and kind.endswith('List') and 'items' in result:
                result = result['items']
                if not result:
                    error_message = f"{kind.replace('List', '')}s not found"
                    self.output_streamer.stream(error_message, "error")
                    raise ResourceNotFound(error_message)
                output_message = f"{kind.replace('List', '')}s found"
                output_type = "name"
            self._generate_output(result, output_message, output_type)
