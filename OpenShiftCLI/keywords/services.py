from kubernetes import config
from openshift.dynamic import DynamicClient
from robotlibcore import keyword
from robot.api import logger
from typing import List

ROBOT_LIBRARY_DOC_FORMAT = 'reST'


class ServiceKeywords(object):
    k8s_client = config.new_client_from_config()
    dyn_client = DynamicClient(k8s_client)
    services = dyn_client.resources.get(api_version='v1', kind='Service')

    @keyword
    def get_services(self, namespace: str='') -> List[str]:
        """
        Get All services
        """
        service_list = self.services.get(namespace=namespace)
        services_found = [service.metadata.name for service in service_list.items]
        logger.info(services_found)
        return services_found

    @keyword
    def services_should_contain(self, servicename: str, namespace: str = '') -> str:
        """
        Get services starting with name servicename

        Args:
          servicename: starting name of the service
          namespace: namespace

        Returns:
          output(List): Values of service names and status with List
        """
        service_list = self.services.get(namespace=namespace)
        service_found = [{service.metadata.name: f'{service.spec.clusterIPs}:{service.spec.ports}'} for service in service_list.items]
        logger.info(service_found)
        return service_found
