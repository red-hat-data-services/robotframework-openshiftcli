from robotlibcore import keyword
from robot.api import logger
from typing import Union
import yaml
import os


class SecretKeywords(object):
    def __init__(self, cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def create_secret(self, filename: str, namespace: Union[str, None] = None) -> None:
        """Create a secret imperative mode

        Args:
            filename (str): path to yaml file with the secret
            namespace (Union[str,None], optional): Namespace. Defaults to None.
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            secret_data = yaml.load(file, yaml.SafeLoader)
            logger.info(secret_data)
            secret = self.cliclient.create(body=secret_data, namespace=namespace)
            logger.info(secret)

    @keyword
    def apply_secret(self, filename: str, namespace: Union[str, None] = None) -> None:
        """Apply a secret Declarative mode

        Args:
            filename (str): path to yaml file with the secret
            namespace (Union[str,None], optional): Namespace. Defaults to None.
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            secret_data = yaml.load(file, yaml.SafeLoader)
        secret = self.cliclient.apply(body=secret_data, namespace=namespace)
        logger.info(secret)

    @keyword
    def delete_secret(self, filename: str, namespace: Union[str, None] = None) -> None:
        """Delete secret

        Args:
            filename (str): path to yaml file with the secret to delete
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            secret_data = yaml.load(file, yaml.SafeLoader)
        del_secret = self.cliclient.delete(secret_data, namespace=namespace)
        logger.info(del_secret)
