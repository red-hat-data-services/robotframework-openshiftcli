from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger, Error
from typing import List, Dict, Union
import json


class KFDEFKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def delete_kfdef(self, name: str, namespace: Union[str, None] = None, **kwargs: str) -> None:
        """Delete KfDef

        Args:
            name (str): KfDef to delete
            namespace (Union[str, None], optional): Namespace where the KfDef exists. Defaults to None.
        """
        result = self.cliclient.delete(name=name, namespace=namespace, **kwargs)
        logger.info(result)

    @keyword
    def get_kfdefs(self, namespace: Union[str, None] = None) -> List[Dict[str, str]]:
        """Get KfDefs

        Args:
            namespace (Union[str, None], optional): Namespace where KfDefs exist. Defaults to None.

        Raises:
            Error: Raises error if no KfDefs found

        Returns:
            List[Dict[str, str]]: List of KfDef names and status
        """
        kfdef_list = self.cliclient.get(name=None, namespace=namespace, label_selector=None)
        if not kfdef_list:
            logger.error('Kfdef not found')
            raise Error('Kfdef not found')
        result = [{"name": kfdef.metadata.name, "status": kfdef.status.conditions} for kfdef in kfdef_list.items]
        logger.info(result)
        return result

    @keyword
    def patch_kfdef(self, name: Union[str, None] = None, body: Union[str, None] = None,
                    namespace: Union[str, None] = None, **kwargs: str) -> None:
        """Delete KfDef

        Args:
            name (Union[str, None], optional): KfDef to delete. Defaults to None.
            body (Union[str, None], optional): KfDef definition file. Defaults to None.
            namespace (Union[str, None], optional): Namespace where the KfDef exists. Defaults to None.
        """
        kfdef_data = json.loads(body)
        result = self.cliclient.patch(name=name, body=kfdef_data, namespace=namespace,
                                      content_type='application/merge-patch+json')
        logger.info(result)
