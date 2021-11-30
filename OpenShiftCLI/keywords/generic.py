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
from OpenShiftCLI.templateloader import TemplateLoader


class GenericKeywords(object):
    def __init__(self, client: GenericClient, data_loader: DataLoader,
                 data_parser: DataParser, output_formatter: OutputFormatter,
                 output_streamer: OutputStreamer, template_loader: TemplateLoader) -> None:
        self.client = client
        self.data_loader = data_loader
        self.data_parser = data_parser
        self.output_formatter = output_formatter
        self.output_streamer = output_streamer
        self.template_loader = template_loader

    @keyword
    def apply(self, kind: str, src: str, namespace: Optional[str] = None,
              **kwargs: Optional[str]) -> List[Dict[str, Any]]:
        """Applies Resource/s definition/s on one or more Resources

        Args:
            kind (str): Resource/s kind/s
            src (str): Path/Url/String containing the yaml or json with the Resource/s definition/s
            namespace (Optional[str], optional): Namespace where the Resource/s exist/s or will be
                                       created. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List containing the apply operation/s result/s
        """
        return self._apply_or_create(kind, 'apply', src, namespace=namespace, **kwargs)

    @keyword
    def create(self, kind: str, src: str, namespace: Optional[str] = None,
               **kwargs: Optional[str]) -> List[Dict[str, Any]]:
        """Creates one or multiple Resources

        Args:
            kind (str): Resource/s kind/s
            src (str): Path/Url/String containing the yaml or json with the Resource/s definition/s
            namespace (Optional[str], optional): Namespace where the Resource/s will be created. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List containing the create operation/s result/s
        """
        return self._apply_or_create(kind, 'create', src, namespace=namespace, **kwargs)

    @keyword
    def delete(self, kind: str, src: Optional[str] = None, name: Optional[str] = None,
               namespace: Optional[str] = None, label_selector: Optional[str] = None,
               field_selector: Optional[str] = None, **kwargs: str) -> List[Dict[str, Any]]:
        """Deletes one or more Resources

        Args:
            kind (str): Resource/s kind/s
            src (str): Path/Url/String containing the yaml or json with the Resource/s definition/s
            name (Optional[str], optional): Name of the Resource to delete
            namespace (Optional[str], optional): Namespace where the Resource/s to delete exist/s. Defaults to None.
            label_selector (Optional[str], optional): Label Selector of the Resource/s to delete. Defaults to None.
            field_selector (Optional[str], optional): Field Selector of the Resource/s to delete. Defaults to None.


        Returns:
            List[Dict[str, Any]]: List containing the delete operation/s result/s
        """
        operation = 'delete'
        if not kind and not (src or name or label_selector or field_selector):
            self._handle_error(operation, ("Kind and src or kind and at least one of name, label_selector "
                                           "or field_selector is required"))
        if kind and not (src or name or label_selector or field_selector):
            self._handle_error(operation, ("Src or at least one of name, label_selector "
                                           "or field_selector is required"))

        if src and (name or label_selector or field_selector):
            self._handle_error(operation, ("Src or at least one of name, label_selector "
                                           "or field_selector is required, but not both"))
        result: List[Dict[str, Any]]
        if src and not (name or label_selector or field_selector):
            items = self._get_items(operation, src, kwargs.pop('template_data', None))
            if kind == 'List':
                result = [self._operate(kind, operation, body=item,
                                        namespace=namespace or item.get('metadata', {}).get('namespace'),
                                        **kwargs) for item in items]
            else:
                result = [self._operate(kind, operation,
                                        name=item.get('metadata', {}).get('name'),
                                        namespace=namespace or item.get('metadata', {}).get('namespace'),
                                        label_selector=item.get('metadata', {}).get('label_selector'),
                                        field_selector=item.get('metadata', {}).get('field_selector'),
                                        **kwargs) for item in items]
        if not src and (name or label_selector or field_selector):
            result = [self._operate(kind, operation, name=name,
                                    namespace=namespace, label_selector=label_selector,
                                    field_selector=field_selector, **kwargs)]
        self._generate_output(operation, result)
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
        operation = 'get'
        arguments = {'name': name, 'namespace': namespace, 'label_selector': label_selector,
                     'field_selector': field_selector, **kwargs}
        result = self._operate(kind, operation, **arguments).get('items')
        if not result:
            self._handle_error(operation, "Not Found")
        self._generate_output(operation, result)
        return result
    
    @keyword
    def get_pod_logs(self, name: str, namespace: str, **kwargs: Optional[str]) -> str:
        result = None
        operation = 'get pod logs'
        try: 
            result = self.client.get_pod_logs(name, namespace, **kwargs)
        except Exception as error:
            self._handle_error(operation, error)
        self._generate_output(operation, result)
        return result
    
    @keyword
    def patch(self, kind: str, src: str, name: str, namespace: Optional[str] = None,
              **kwargs: str) -> Dict[str, Any]:
        """Updates Fields of the Resource using JSON merge patch

        Args:
            kind (str): Resource kind
            src (str): Path/Url/String containing the json with the Resource patch
            name (str): Name of Resource to patch
            namespace (Optional[str], optional): Namespace where the Resource Exists. Defaults to None.

        Returns:
            Dict[str, Any]: Patch operation result
        """
        operation = 'patch'
        if not (kind and src and name):
            self._handle_error(operation, "Kind, src and name are required")
        if kind and not (src and name):
            self._handle_error(operation, "Src and name are required")
        body = self._parse_data(operation, self._load_data(operation, src))[0]
        arguments = {'name': name, 'body': body, 'namespace': namespace,
                     'content_type': 'application/merge-patch+json', **kwargs}
        result = self._operate(kind, operation, **arguments)
        self._generate_output(operation, result)
        return result

    @keyword
    def watch(self, kind: str, namespace: Optional[str] = None, name: Optional[str] = None,
              label_selector: Optional[str] = None, field_selector: Optional[str] = None,
              resource_version: Optional[str] = None,
              timeout: Optional[int] = 60) -> List[Dict[str, Any]]:
        """Watches changes in one or more Resources

        Args:
            kind (str): Resource/s kind/s
            name (Optional[str], optional): Resource name. Defaults to None.
            namespace (Optional[str], optional): Namespace where the Resource/s exist/s. Defaults to None.
            label_selector (Optional[str], optional): Label Selector of the Resource/s. Defaults to None.
            field_selector (Optional[str], optional): Field Selector of the Resource/s. Defaults to None.
            resource_version (Optional[str], optional): Resource Version of the Resource/s. Defaults to None.
            timeout (Optional[int], optional): Timeout for the watch. Defaults to 60.

        Returns:
            List[Dict[str, Any]]: List containing the list of watched events
        """
        operation = 'watch'
        if not kind:
            self._handle_error(operation, "Kind is required")
        arguments = {'name': name, 'namespace': namespace, 'label_selector': label_selector,
                     'field_selector': field_selector, 'resource_version': resource_version,
                     'timeout': timeout}
        result = self._operate(kind, operation, **arguments)
        self._generate_output(operation, result)
        return result

    def _apply_or_create(self, kind: str, operation: str, src: str, namespace: Optional[str] = None,
                         **kwargs: Optional[str]) -> List[Dict[str, Any]]:
        if not (kind and src):
            self._handle_error(operation, "Kind and src are required")
        items = self._get_items(operation, src, kwargs.pop('template_data', None))
        result = [self._operate(kind, operation, body=item,
                                namespace=namespace or item.get('metadata', {}).get('namespace'),
                                **kwargs) for item in items]
        self._generate_output(operation, result)
        return result

    def _get_items(self, operation: str, src: str, template_data: Optional[str] = None) -> List[Dict[str, Any]]:
        loaded_data = self._load_data(operation, src)
        data = self._load_template_data(operation, loaded_data, template_data) if template_data else loaded_data
        items = self._parse_data(operation, data)
        return items

    def _load_data(self, operation: str, src: str) -> str:
        if os.path.isfile(src):
            try:
                return self.data_loader.from_file(src)
            except Exception as error:
                self._handle_error(operation, f"Load data from file failed\n{error}")
        if validators.url(src):
            try:
                return self.data_loader.from_url(src)
            except Exception as error:
                self._handle_error(operation, f"Load data from url failed\n{error}")
        return src

    def _load_template_data(self, operation: str, data: str, template_data: str) -> str:
        result: str
        try:
            result = self.template_loader.from_jinja2(data, template_data)
        except Exception as error:
            self._handle_error(operation, f"Load data from jinja failed\n{error}")
        return result

    def _parse_data(self, operation: str, data: str) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]]
        if self._is_valid_json(data):
            try:
                result = self.data_parser.from_json(data)
            except Exception as error:
                self._handle_error(operation, f"Parse json failed\n{error}")
        elif self._is_valid_yaml(data):
            try:
                result = self.data_parser.from_yaml(data)
            except Exception as error:
                self._handle_error(operation, f"Parse yaml failed\n{error}")
        else:
            self._handle_error(operation, f"Data is not a valid yaml or json")
        return result

    def _operate(self, kind: str, operation: str, **arguments: Optional[str]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        result: Union[Dict[str, Any], List[Dict[str, Any]]]
        try:
            result = getattr(self.client, operation)(kind, **arguments)
        except Exception as error:
            self._handle_error(operation, error)
        return result

    def _handle_error(self, operation: str, error_reason: str) -> None:
        error_message = f"{operation.capitalize()} failed\nReason: {error_reason}"
        self.output_streamer.stream(error_message, 'error')
        raise ResourceOperationFailed(error_message)

    def _generate_output(self, operation: str,
                         output: Union[List[List[Dict[str, Any]]], List[Dict[str, Any]]]) -> None:
        output_message = f"{operation.capitalize()} result"
        output = self.output_formatter.format(output, output_message, None)
        self.output_streamer.stream(output, 'info')

    def _is_valid_json(self, data: str) -> bool:
        try:
            json.loads(data)
        except Exception as e:
            return False
        return True

    def _is_valid_yaml(self, data: str) -> bool:
        try:
            yaml.safe_load_all(data)
        except Exception as e:
            return False
        return True
