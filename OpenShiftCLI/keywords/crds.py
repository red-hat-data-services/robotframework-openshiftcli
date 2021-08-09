from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Union


class CRDKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def delete_crd(self, name: str, namespace: Union[str, None] = None, **kwargs: str) -> None:
        """Delete Custom Resource Definition

        Args:
            name (str): Custom Resource Definition to delete
            namespace (Union[str, None], optional): Namespace where the CRD exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)
