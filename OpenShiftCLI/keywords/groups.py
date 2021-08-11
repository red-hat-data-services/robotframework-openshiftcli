import os
import yaml
from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger


class GroupKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_group(self, filename: str) -> None:
        """Create Group

        Args:
            filename (str): Path to the yaml file containing the Group definition
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            group_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=group_data, namespace=None)
        logger.info(result)

    @keyword
    def delete_group(self, name: str, **kwargs: str) -> None:
        """Delete Group

        Args:
            name (str): Group to delete
        """
        result = self.cliclient.delete(name=name, namespace=None, **kwargs)
        logger.info(result)
