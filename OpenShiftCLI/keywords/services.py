from kubernetes import config
from openshift.dynamic import DynamicClient
from robotlibcore import keyword
from robot.api import logger, Error
from typing import Dict, List


class ServiceKeywords(object):
    def __init__(self) -> None:
        self.k8s_client = config.new_client_from_config()
        self.dyn_client = DynamicClient(self.k8s_client)
        self.services = self.dyn_client.resources.get(api_version='v1', kind='Service')

    @keyword
    def get_services(self, namespace: str = '') -> List[str]:
        """Get all services

        Args:
            namespace (str, optional): Namespace. Defaults to ''.

        Raises:
            Error: Service not found

        Returns:
            List[str]: List with all Services
        """
        service_list = self.services.get(namespace=namespace)
        services_found = [service.metadata.name for service in service_list.items]
        if not services_found:
            logger.error(f'Services not found in {namespace}')
            raise Error(
                f'Services not found in {namespace}'
            )
        logger.info(services_found)
        return services_found

    @keyword
    def services_should_contain(self, servicename: str, namespace: str = '') -> List[Dict[str, str]]:
        """
        Get services starting with name servicename

        Args:
          servicename: starting name of the service
          namespace: namespace

        Returns:
          output(List): Values of service names and status with List
        """
        service_list = self.services.get(name=servicename, namespace=namespace)
        service_found = [{service.metadata.name: f'{service.spec.clusterIPs}:{service.spec.ports}'}
                         for service in service_list.items]
        if not service_found:
            logger.error(f'Pod {servicename} not found')
            raise Error(
                f'Pod {servicename} not found'
            )
        logger.info(service_found)
        return service_found
