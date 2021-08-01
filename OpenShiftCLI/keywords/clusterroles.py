from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Union


class ClusterroleKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def delete_cluster_role(self, name: Union[str, None], **kwargs: str) -> None:
        """Delete Cluster Role

            Args:
                name (str): Cluster Role to delete
            """
        result = self.cliclient.delete(name=name, namespace=None, **kwargs)
        logger.info(result)
