from robotlibcore import keyword
from robot.api import logger
import yaml
import os
from typing import Union


class ListKeywords(object):
    def __init__(self, cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_oclist(self, filename: str, namespace: Union[str, None] = None) -> None:
        """Create an Object list in Openshift

        Args:
            filename (str): Path to the list of object
            namespace (str, optional): Namespace. Defaults to None.
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            list_data = yaml.load(file, yaml.SafeLoader)
            logger.info(list_data)
            list = self.cliclient.create(body=list_data, namespace=namespace)
            logger.info(list)

    @keyword
    def apply_oclist(self, filename: str, namespace: Union[str, None] = None) -> None:
        """Apply Objects list in Openshift (Declarative Mode)

        Args:
            filename (str): Path to the list of object
            namespace (str, optional): Namespace. Defaults to None.
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            list_data = yaml.load(file, yaml.SafeLoader)
        list = self.cliclient.apply(body=list_data, namespace=namespace)
        logger.info(list)

    @keyword
    def delete_objects_list(self, filename: str, namespace: Union[str, None] = None) -> None:
        """Delete objects list in Openshift

        Args:
            filename (str): Path to the list of object
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            list_data = yaml.load(file, yaml.SafeLoader)
        del_objects = self.cliclient.delete(list_data, namespace=namespace)
        logger.info(del_objects)
