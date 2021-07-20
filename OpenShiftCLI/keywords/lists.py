from kubernetes import config
from openshift.dynamic import DynamicClient
from robotlibcore import keyword
from robot.api import logger
import yaml
import os


class ListKeywords(object):
    def __init__(self) -> None:
        self.k8s_client = config.new_client_from_config()
        self.dyn_client = DynamicClient(self.k8s_client)
        self.lists = self.dyn_client.resources.get(api_version='v1', kind='List')

    @keyword
    def create_oclist(self, filename: str, namespace: str = "") -> None:
        """Create an Object list in Openshift

        Args:
            filename (str): Path to the list of object
            namespace (str, optional): Namespace. Defaults to None.
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            list_data = yaml.load(file, yaml.SafeLoader)
            logger.info(list_data)
            list = self.lists.create(body=list_data, namespace=namespace)
            logger.info(list)

    @keyword
    def apply_oclist(self, filename: str, namespace: str = "") -> None:
        """Apply Objects list in Openshift (Declarative Mode)

        Args:
            filename (str): Path to the list of object
            namespace (str, optional): Namespace. Defaults to None.
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            list_data = yaml.load(file, yaml.SafeLoader)
        list = self.lists.apply(body=list_data, namespace=namespace)
        logger.info(list)

    @keyword
    def delete_objects_list(self, filename: str) -> None:
        """Delete objects list in Openshift

        Args:
            filename (str): Path to the list of object
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            list_data = yaml.load(file, yaml.SafeLoader)
        del_objects = self.lists.delete(list_data)
        logger.info(del_objects)
