import os

import yaml
from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger


class ClusterroleKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_cluster_role(self, filename: str) -> None:
        """Create Cluster Role

        Args:
            filename (str): Path to the yaml file containing the Cluster Role definition
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            cluster_role_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=cluster_role_data, namespace=None)
        logger.info(result)

    @keyword
    def delete_cluster_role(self, name: str, **kwargs: str) -> None:
        """Delete Cluster Role

            Args:
                name (str): Cluster Role to delete
            """
        result = self.cliclient.delete(name=name, namespace=None, **kwargs)
        logger.info(result)
