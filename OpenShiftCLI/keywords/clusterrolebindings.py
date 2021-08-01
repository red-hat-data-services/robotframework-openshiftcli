from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger


class ClusterrolebindingKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def delete_cluster_role_binding(self, name: str, **kwargs: str) -> None:
        """Delete Cluster Role Binding

        Args:
            name (str): Cluster Role Binding to delete
        """
        result = self.cliclient.delete(name=name, namespace=None, **kwargs)
        logger.info(result)
