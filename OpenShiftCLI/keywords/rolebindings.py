from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Union


class RolebindingKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def delete_role_binding(self, name: str, namespace: Union[str, None] = None, **kwargs) -> None:
        """Delete Role Bindig

        Args:
            name (str): Role Binding to delete
            namespace (Union[str, None], optional): Namespace where the Role Binding exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)
