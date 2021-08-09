from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Union


class ConfigmapKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def delete_configmap(self, name: str, namespace: Union[str, None] = None, **kwargs: str) -> None:
        """Delete ConfigMap

        Args:
            name (str): ConfigMap to be deleted
            namespace (Union[str, None], optional): Namespace where the ConfigMap exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)
