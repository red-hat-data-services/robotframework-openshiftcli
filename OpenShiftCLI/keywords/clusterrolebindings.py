import os
import yaml
from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger


class ClusterrolebindingKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_cluster_role_binding(self, filename: str) -> None:
        """Create Cluster Role Binding

        Args:
            filename (str): Path to the yaml file containing the Cluster Role Binding definition
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            cluster_role_binding_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=cluster_role_binding_data, namespace=None)
        logger.info(result)

    @keyword
    def delete_cluster_role_binding(self, name: str, **kwargs: str) -> None:
        """Delete Cluster Role Binding

        Args:
            name (str): Cluster Role Binding to delete
        """
        result = self.cliclient.delete(name=name, namespace=None, **kwargs)
        logger.info(result)
