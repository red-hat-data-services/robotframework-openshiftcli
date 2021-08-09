from OpenShiftCLI.cliclient import Cliclient
from robotlibcore import keyword
from robot.api import logger, Error
from typing import List, Dict, Union
import os
import yaml


class ProjectKeywords(object):
    def __init__(self, cliclient: Cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def apply_project(self, name: str) -> None:
        """Create a project in declarative mode

        Args:
            name (str): Project name
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{name}') as file:
            project = yaml.load(file, yaml.SafeLoader)
        apply_project = self.cliclient.apply(body=project, namespace=None)
        logger.info(apply_project)

    @keyword
    def delete_project(self, name: str, **kwargs: str) -> None:
        """Delete Project

        Args:
            name (str): Project to delete
        """
        result = self.cliclient.delete(name=name, namespace=None, **kwargs)
        logger.info(result)

    @keyword
    def get_projects(self) -> List[str]:
        """Get All Projects

        Returns:
            List[str]: List of Project names
        """
        project_list = self.cliclient.get(name=None, namespace=None)
        result = [project.metadata.name for project in project_list.items]
        logger.info(result)
        return result

    @keyword
    def new_project(self, name: str) -> None:
        """Create new Project

        Args:
            name (str): Project name
        """
        project = f"""
      apiVersion: project.openshift.io/v1
      kind: Project
      metadata:
        name: {name}
      spec:
        finalizers:
          - kubernetes
      """
        project_data = yaml.load(project, yaml.SafeLoader)
        new_project = self.cliclient.create(body=project_data, namespace=None)
        logger.info(new_project)

    @keyword
    def projects_should_contain(self, name: str) -> Dict[str, str]:
        """
        Get projects starting with name

        Args:
          name: name of the project

        Returns:
          output(Dictionary): Values of project names and status in a List
        """
        project_list = self.cliclient.get(name=name, namespace=None)
        project_found = {project_list.metadata.name: project_list.status.phase}
        if not project_found:
            logger.error(f'Pod {name} not found')
            raise Error(
                f'Pod {name} not found'
            )
        logger.info(project_found)
        return project_found

    @keyword
    def wait_until_project_exists(self, name: Union[str, None] = None, timeout: Union[int, None] = 100) -> None:
        """Wait until a Project exists

        Args:
            name (Union[str, None], optional): Project to wait for. Defaults to None.
            timeout (Union[int, None], optional): Time to wait. Defaults to 100.
        """
        for event in self.cliclient.watch(namespace=None, name=None, timeout=timeout):
            if event['object'].metadata.name == name:
                logger.info(f"Project {name} found")
                logger.info(f'{event["object"].metadata.name}\nStatus:{event["object"].status.phase}')
                break
