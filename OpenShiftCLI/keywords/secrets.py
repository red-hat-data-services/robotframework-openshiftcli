from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger
from typing import Union
import os
import yaml


class SecretKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

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
    def delete_secret(self, name: str, namespace: Union[str, None] = None, **kwargs: str) -> None:
        """Delete Secret

        Args:
            name (str): Secret to delete.
            namespace (Union[str, None], optional): Namespace where the Secret exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)

    @keyword
    def delete_secret_from_file(self, filename: str, namespace: Union[str, None] = None, **kwargs: str) -> None:
        """Delete Secret From File

        Args:
            filename (str): File containing the definition of the Secret to delete
            namespace (Union[str, None], optional): Namespace where the Secret exists. Defaults to None.
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{filename}') as file:
            secret_data = yaml.load(file, yaml.SafeLoader)
        result = self.cliclient.delete(name=secret_data['metadata']['name'],
                                       namespace=namespace or secret_data['metadata']['namespace'], **kwargs)
        logger.info(result)
