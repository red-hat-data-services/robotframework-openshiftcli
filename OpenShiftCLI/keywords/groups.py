from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger


class GroupKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def delete_group(self, name: str, **kwargs: str) -> None:
        """Delete Group

        Args:
            name (str): Group to delete
        """
        result = self.cliclient.delete(name=name, namespace=None, **kwargs)
        logger.info(result)
