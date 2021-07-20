from robotlibcore import keyword
from robot.api import logger, Error
from typing import List, Dict, Union
import yaml
import os


class ProjectKeywords(object):
    def __init__(self, cliclient) -> None:
        self.cliclient = cliclient

    @keyword
    def get_projects(self) -> List[str]:
        """
        Get All Projects

        Args:
          None

        Returns:
          output(List): Values of project names in a List
        """
        project_list = self.cliclient.get()
        projects = [project.metadata.name for project in project_list.items]
        logger.info(projects)
        return projects

    @keyword
    def projects_should_contain(self, projectname: str) -> Dict[str, str]:
        """
        Get pods starting with name podname

        Args:
          projectname: name of the project

        Returns:
          output(Dictionary): Values of project names and status in a List
        """
        project_list = self.cliclient.get(name=projectname)
        project_found = {project_list.metadata.name: project_list.status.phase}
        if not project_found:
            logger.error(f'Pod {projectname} not found')
            raise Error(
                f'Pod {projectname} not found'
            )
        logger.info(project_found)
        return project_found

    @keyword
    def new_project(self, projectname: str) -> None:
        """Create new Project

        Args:
            projectname (str): Project name
        """
        project = f"""
      apiVersion: project.openshift.io/v1
      kind: Project
      metadata:
        name: {projectname}
      spec:
        finalizers:
          - kubernetes
      """
        project_data = yaml.load(project, yaml.SafeLoader)
        new_project = self.cliclient.create(body=project_data)
        print(new_project)

    @keyword
    def delete_project(self, projectname: str) -> None:
        """Delete Openshift Project

        Args:
            projectname (str): Project to be deleted
        """
        del_project = self.cliclient.delete(projectname)
        print(del_project)

    @keyword
    def apply_project(self, projectname: str) -> None:
        """Create a project in declarative mode

        Args:
            projectname (str): Project name
        """
        cwd = os.getcwd()
        with open(rf'{cwd}/{projectname}') as file:
            project = yaml.load(file, yaml.SafeLoader)
        apply_project = self.cliclient.apply(body=project)
        print(apply_project)

    @keyword
    def wait_until_project_exists(self, projectname: Union[str, None] = None, timeout: Union[int, None] = 100) -> None:
        """Wait until a project exist in Openshift

        Args:
            projectname (Union[str, None], optional): Project to wait. Defaults to None.
            timeout (Union[int, None], optional): Time to wait. Defaults to 100.
        """
        projects = self.cliclient.dyn_client.resources.get(api_version='v1', kind='Namespace')
        project = projects.watch(namespace='', timeout=timeout)

        for event in project:
            if event['object'].metadata.name == projectname:
                logger.info(f"Project {projectname} found")
                logger.info(f'{event["object"].metadata.name}\nStatus:{event["object"].status.phase}')
                break
