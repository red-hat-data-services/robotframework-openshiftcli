from robotlibcore import keyword
from robot.api import logger, Error
from typing import Dict, List, Union


class ServiceKeywords(object):
    def __init__(self, cliclient) -> None:
        self.cliclient = cliclient

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
        service_list = self.cliclient.get(name=None, namespace=namespace)
        services_found = [service.metadata.name for service in service_list.items]
        if not services_found:
            logger.error(f'Services not found in {namespace}')
            raise Error(
                f'Services not found in {namespace}'
            )
        logger.info(services_found)
        return services_found

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
        service_list = self.cliclient.get(name=name, namespace=namespace)
        service_found = [{service.metadata.name: f'{service.spec.clusterIPs}:{service.spec.ports}'}
                         for service in service_list.items]
        if not service_found:
            logger.error(f'Pod {name} not found')
            raise Error(
                f'Pod {name} not found'
            )
        logger.info(service_found)
        return service_found
