from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Union
import os
import yaml


class ListKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def apply_objects_list(self, filename: str, namespace: Union[str, None] = None) -> None:
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
    def create_objects_list(self, filename: str, namespace: Union[str, None] = None) -> None:
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
    def delete_objects_list_from_file(self, filename: str, namespace: Union[str, None] = None) -> None:
        """Delete List of Objects From File

        Args:
            filename (str): Path to the List of Objects to delete
            namespace (Union[str, None], optional): Namespace where the List of Objects exists. Defaults to None.
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            list_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.delete_from_file(body=list_data, namespace=namespace)
        logger.info(result)
