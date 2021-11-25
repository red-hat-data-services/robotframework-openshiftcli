import json
import os
import validators
import yaml

from typing import Any, Dict, List, Optional, Union

from robotlibcore import keyword

from OpenShiftCLI.cliclient import GenericClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.errors import ResourceOperationFailed
from OpenShiftCLI.outputformatter import OutputFormatter
from OpenShiftCLI.outputstreamer import OutputStreamer


class GenericKeywords(object):
    def __init__(self, client: GenericClient, data_loader: DataLoader, data_parser: DataParser,
                 output_formatter: OutputFormatter, output_streamer: OutputStreamer) -> None:
        self.client = client
        self.data_loader = data_loader
        self.data_parser = data_parser
        self.output_formatter = output_formatter
        self.output_streamer = output_streamer
        
    @keyword
    def apply(self, kind: str, src: str = None, namespace: Optional[str] = None,
              **kwargs: Optional[str]) -> List[Dict[str, Any]]:
        """Applies definition/s from file on one or more resources

        Args:
            kind (str): Resource/s kind/s
            src (str): Path/Url/String containing the yaml with the Resource/s definition/s
            namespace (str, optional): Namespace where the Resource/s exist/s or will be
                                       created. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List containing the apply operation/s result/s
        """
        return self._apply_or_create(kind=kind, operation='apply', src=src,
                                     namespace=namespace, **kwargs)

    @keyword
    def create(self, kind: str, src: str = None, namespace: Optional[str] = None,
               **kwargs: Optional[str]) -> List[Dict[str, Any]]:
        """Creates one or multiple resources

        Args:
            kind (str): Resource/s kind/s
            src (str): Path/Url/String containing the yamm with the Resource/s definition/s
            namespace (Optional[str], optional): Namespace where the Resource/s will be created. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List containing the create operation/s result/s
        """
        return self._apply_or_create(kind=kind, operation='create', src=src,
                                     namespace=namespace, **kwargs)

    @keyword
    def delete(self, kind: str, src: Optional[str] = None, name: Optional[str] = None,
               namespace: Optional[str] = None, label_selector: Optional[str] = None,
               field_selector: Optional[str] = None, **kwargs: str) -> List[Dict[str, Any]]:
        """Deletes one or more Resources

        Args:
            kind (str): Resource/s kind/s
            src (str): Path/Url/String containing the yaml with the Resource/s definition/s
            name (Optional[str], optional): Name of the Resource/s to delete
            namespace (Optional[str], optional): Namespace where the Resource/s to delete exist/s. Defaults to None.
            label_selector (Optional[str], optional): Label Selector of the Resource/s to delete. Defaults to None.
            field_selector (Optional[str], optional): Field Selector of the Resource/s to delete. Defaults to None.


        Returns:
            List[Dict[str, Any]]: List containing the delete operation/s result/s
        """
        if not (src or name or label_selector or field_selector):
            self._handle_error(operation='delete',
                               error_reason=("Src or at least one of name, label_selector "
                                             "or field_selector is required"))
        if src and (name or label_selector or field_selector):
            self._handle_error(operation='delete',
                               error_reason=("Src or at least one of name, label_selector "
                                             "or field_selector is required, but not both"))
        result = []
        if src and not (name or label_selector or field_selector):
            items = self._get_items(operation='delete', src=src, kind=kind, data_type='yaml')
            if kind == 'List':
                result = [self._operate(kind=kind, operation='delete', body=item,
                                        namespace=namespace or item.get('metadata', {}).get('namespace'),
                                        **kwargs) for item in items]
            else:
                result = [self._operate(kind=kind, operation='delete',
                                        name=item.get('metadata', {}).get('name'),
                                        namespace=namespace or item.get('metadata', {}).get('namespace'),
                                        label_selector=item.get('metadata', {}).get('label_selector'),
                                        field_selector=item.get('metadata', {}).get('field_selector'),
                                        **kwargs) for item in items]
        if not src and (name or label_selector or field_selector):
            result = [self._operate(kind=kind, operation='delete', name=name,
                                    namespace=namespace, label_selector=label_selector,
                                    field_selector=field_selector, **kwargs)]
        self._generate_output(output=result, output_message="Delete result", output_type=None)
        return result

    @keyword
    def get(self, kind: str, name: Optional[str] = None, namespace: Optional[str] = None,
            label_selector: Optional[str] = None, field_selector: Optional[str] = None,
            **kwargs: str) -> List[Dict[str, Any]]:
        """Gets Resource/s

        Args:
            kind (str): Resource/s kind/s
            name (Optional[str], optional): Resource name. Defaults to None.
            namespace (Optional[str], optional): Namespace where the Resource/s exist/s. Defaults to None.
            label_selector (Optional[str], optional): Label Selector of the Resource/s. Defaults to None.
            field_selector (Optional[str], optional): Field Selector of the Resource/s. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List containing the get operation/s result/s
        """
        arguments = {'name': name, 'namespace': namespace, 'label_selector': label_selector,
                     'field_selector': field_selector, **kwargs}
        result = self._operate(kind=kind, operation='get', **arguments).get('items')
        if not result:
            self._handle_error(operation='get', error_reason="Not Found")
        self._generate_output(output=result, output_message="Get result", output_type=None)
        return result

    @keyword
    def get_pod_logs(self, name: str, namespace: str, **kwargs: Optional[str]) -> None:
        result = None
        try: 
            result = self.client.get_pod_logs(name=name, namespace=namespace, **kwargs)
        except Exception as error:
            self._handle_error(operation='get pod logs', error_reason=error)
        self.output_streamer.stream(type(result), 'info')
        self._generate_output(output=result, output_message="Get Pod Logs result", output_type=None)

    @keyword
    def patch(self, kind: str, src: str = None, name: Optional[str] = None,
              namespace: Optional[str] = None, **kwargs: str) -> List[Dict[str, Any]]:
        """Updates Fields of the Resource using JSON merge patch

        Args:
            kind (str): Resource kind
            src (str): Path/Url/String containing the json  with the Resource patch
            name (Optional[str], optional): Name of Resource to patch
            namespace (Optional[str], optional): Namespace where the Resource Exists. Defaults to None.

        Returns:
            Dict[str, Any]: [description]
        """
        if not (src and name):
            self._handle_error('patch', "Src and name required")
        items = self._get_items(operation='patch', src=src, kind=kind, data_type='json')
        result = [self._operate(kind=kind, operation='patch', name=name, body=item,
                                namespace=namespace, content_type='application/merge-patch+json',
                                **kwargs) for item in items]
        self._generate_output(output=result, output_message="Patch result", output_type=None)
        return result

    @keyword
    def watch(self, kind: str, namespace: Optional[str] = None, name: Optional[str] = None,
              label_selector: Optional[str] = None, field_selector: Optional[str] = None,
              resource_version: Optional[str] = None,
              timeout: Optional[int] = 60) -> List[Dict[str, Any]]:
        """Watches changes to a one or more Resources

        Args:
            kind (str): Resource/s kind/s
            name (Optional[str], optional): Resource name. Defaults to None.
            namespace (Optional[str], optional): Namespace where the Resource/s exist/s. Defaults to None.
            label_selector (Optional[str], optional): Label Selector of the Resource/s. Defaults to None.
            field_selector (Optional[str], optional): Field Selector of the Resource/s. Defaults to None.
            resource_version (Optional[str], optional): Resource Version of the Resource/s. Defaults to None.
            timeout (Optional[int], optional): Timeout for the watch. Defaults to 60.

        Returns:
            List[Dict[str, Any]]: [description]
        """
        arguments = {'name': name, 'namespace': namespace, 'label_selector': label_selector,
                     'field_selector': field_selector, 'resource_version': resource_version,
                     'timeout': timeout}
        result = self._operate(kind=kind, operation='watch', **arguments)
        self._generate_output(output=result, output_message="Watch result", output_type=None)
        return result

    def _apply_or_create(self, kind: str, operation: str, src: str, namespace: Optional[str] = None,
                         **kwargs: Optional[str]) -> List[Dict[str, Any]]:
        if not src:
            self._handle_error(operation, "Src required")
        items = self._get_items(operation=operation, src=src, kind=kind, data_type='yaml')
        result = [self._operate(kind=kind, operation=operation, body=item,
                                namespace=namespace or item.get('metadata', {}).get('namespace'),
                                **kwargs) for item in items]
        self._generate_output(output=result, output_message=f"{operation.capitalize()} result", output_type=None)
        return result

    def _get_items(self, operation: str, src: str, kind: str, data_type: str) -> List[Dict[str, Any]]:
        return self._parse_data(operation, self._get_data(operation, src, kind), data_type)

    def _get_data(self, operation: str, src: str, kind: str) -> str:
        if os.path.isfile(src):
            try:
                return self.data_loader.from_file(path=src)
            except Exception as error:
                self._handle_error(operation=operation,
                                   error_reason=f"Load data from file failed\n{error}")
        if validators.url(src):
            try:
                return self.data_loader.from_url(path=src)
            except Exception as error:
                self._handle_error(operation=operation,
                                   error_reason=f"Load data from url failed\n{error}")
        if ('kind' in yaml.safe_load(src)) or self._validate_json(src):
            return src
        self._handle_error(operation=operation,
                           error_reason="Src is not a valid path, url, yaml or json")

    def _parse_data(self, operation: str, data: str, data_type: str) -> List[Dict[str, Any]]:
        if data_type == 'yaml':
            try:
                return self.data_parser.from_yaml(data=data)
            except Exception as error:
                self._handle_error(operation=operation,
                                   error_reason=f"Data is not a valid yaml\n{error}")
        if data_type == 'json':
            try:
                return self.data_parser.from_json(data=data)
            except Exception as error:
                self._handle_error(operation=operation,
                                   error_reason=f"Data is not a valid json\n{error}")

    def _operate(self, kind: str, operation: str, **arguments) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        try:
            return getattr(self.client, operation)(kind=kind, **arguments)
        except AttributeError as error:
            self._handle_error(operation=operation,
                               error_reason=f"Operation {operation} does not exists\n{error}")
        except Exception as error:
            self._handle_error(operation=operation, error_reason=error)

    def _handle_error(self, operation: str, error_reason: str) -> None:
        error_message = f"{operation.capitalize()} failed\nReason: {error_reason}"
        self.output_streamer.stream(output=error_message, type='error')
        raise ResourceOperationFailed(error_message)

    def _generate_output(self, output: Union[List[List[Dict[str, Any]]], List[Dict[str, Any]]],
                         output_message: str, output_type: Optional[str] = None) -> None:
        output = self.output_formatter.format(output=output, message=output_message,
                                              type=output_type)
        self.output_streamer.stream(output=output, type='info')

    def _validate_json(self, src: str) -> bool:
        try:
            json.loads(src)
        except ValueError:
            return False
        return True
