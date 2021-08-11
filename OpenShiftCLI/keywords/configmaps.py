import os

import yaml
from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Optional, Union


class ConfigmapKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_configmap(self, filename: str, namespace: Optional[str] = None) -> None:
        """Create Configmap

        Args:
            filename (str): Path to the yaml file containing the Configmap definition
            namespace (Optional[str]): Namespace where the Configmap will be created
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            configmap_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=configmap_data, namespace=namespace)
        logger.info(result)

    @keyword
    def delete_configmap(self, name: str, namespace: Union[str, None] = None, **kwargs: str) -> None:
        """Delete ConfigMap

        Args:
            name (str): ConfigMap to be deleted
            namespace (Union[str, None], optional): Namespace where the ConfigMap exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)
