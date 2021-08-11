import os

import yaml
from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Optional


class RoleKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_role(self, filename: str, namespace: Optional[str] = None) -> None:
        """Create Role

        Args:
            filename (str): Path to the yaml file containing the Role definition
            namespace (Optional[str]): Namespace where the Role will be created
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            role_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=role_data, namespace=namespace)
        logger.info(result)

    @keyword
    def delete_role(self, name: str, namespace: Optional[str] = None, **kwargs) -> None:
        """Delete Role

        Args:
            name (str): Role to delete
            namespace (Optional[str]): Namespace where the Role exists
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)
