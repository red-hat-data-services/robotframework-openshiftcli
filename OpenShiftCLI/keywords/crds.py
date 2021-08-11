import os

import yaml
from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Optional, Union


class CRDKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_crd(self, filename: str, namespace: Optional[str] = None) -> None:
        """Create Custom Resource Definition

        Args:
            filename (str): Path to the yaml file containing the Custom Resource Definition definition
            namespace (Optional[str]): Namespace where the Custom Resource Definition will be created
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            crd_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=crd_data, namespace=namespace)
        logger.info(result)

    @keyword
    def delete_crd(self, name: str, namespace: Union[str, None] = None, **kwargs: str) -> None:
        """Delete Custom Resource Definition

        Args:
            name (str): Custom Resource Definition to delete
            namespace (Union[str, None], optional): Namespace where the CRD exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)
