import os

import yaml
from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Optional, Union


class RolebindingKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_role_binding(self, filename: str, namespace: Optional[str] = None) -> None:
        """Create Role Binding

        Args:
            filename (str): Path to the yaml file containing the Role Binding definition
            namespace (Optional[str]): Namespace where the Role Binding will be created
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            role_binding_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=role_binding_data, namespace=namespace)
        logger.info(result)

    @keyword
    def delete_role_binding(self, name: str, namespace: Union[str, None] = None, **kwargs) -> None:
        """Delete Role Bindig

        Args:
            name (str): Role Binding to delete
            namespace (Union[str, None], optional): Namespace where the Role Binding exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)
