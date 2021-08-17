import os

import yaml
from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger, Error
from typing import Dict, List, Optional, Union


class ServiceKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_service(self, filename: str, namespace: Optional[str] = None) -> None:
        """Create Service

        Args:
            filename (str): Path to the yaml file containing the Service definition
            namespace (Optional[str]): Namespace where the Cluster Service will be created
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            service_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=service_data, namespace=namespace)
        logger.info(result)

    @keyword
    def get_services(self, namespace: Union[str, None] = None) -> List[str]:
        """Get all services

        Args:
            namespace (str, optional): Namespace. Defaults to ''.

        Raises:
            Error: Service not found

        Returns:
            List[str]: List with all Services
        """
        service_list = self.cliclient.get(name=None, namespace=namespace, label_selector=None)
        services_found = [service.metadata.name for service in service_list.items]
        if not services_found:
            logger.error(f'Services not found in {namespace}')
            raise Error(
                f'Services not found in {namespace}'
            )
        logger.info(services_found)
        return services_found

    @keyword
    def delete_service(self, name: str, namespace: Union[str, None] = None, **kwargs) -> None:
        """Delete Service

        Args:
            name (str): Service to delete
            namespace (Union[str, None], optional): Namespace where the Service exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)

    @keyword
    def services_should_contain(self, name: str, namespace: Union[str, None] = None) -> List[Dict[str, str]]:
        """
        Get services starting with name name

        Args:
          name: starting name of the service
          namespace: namespace

        Returns:
          output(List): Values of service names and status with List
        """
        service_list = self.cliclient.get(name=name, namespace=namespace, label_selector=None)
        service_found = {service_list.metadata.name: f'{service_list.spec.clusterIPs}:{service_list.spec.ports}'}
        if not service_found:
            logger.error(f'Service {name} not found')
            raise Error(
                f'Service {name} not found'
            )
        logger.info(service_found)
        return service_found
