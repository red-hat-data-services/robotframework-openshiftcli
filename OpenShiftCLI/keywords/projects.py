from kubernetes import config
from openshift.dynamic import DynamicClient
from robotlibcore import keyword
from robot.api import logger
from typing import List, Dict


class ProjectKeywords(object):

    k8s_client = config.new_client_from_config()
    dyn_client = DynamicClient(k8s_client)
    projects = dyn_client.resources.get(api_version='project.openshift.io/v1', kind='Project')

    @keyword
    def get_projects(self) -> List[str]:
        """
        Get All Projects

        Args:
          None

        Returns:
          output(List): Values of project names in a List
        """
        project_list = self.projects.get()
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
        project_list = self.projects.get(name=projectname)
        project_found = {project_list.metadata.name: project_list.status.phase}
        logger.info(project_found)
        return project_found
