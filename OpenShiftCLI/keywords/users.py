import os
import yaml
from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger


class UserKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_user(self, filename: str) -> None:
        """Create User

        Args:
            filename (str): Path to the yaml file containing the User definition
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            user_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.create(body=user_data, namespace=None)
        logger.info(result)

    @keyword
    def delete_user(self, name: str, **kwargs: str) -> None:
        """Delete User

        Args:
            name (str): User to delete
        """
        result = self.cliclient.delete(name=name, namespace=None, **kwargs)
        logger.info(result)
