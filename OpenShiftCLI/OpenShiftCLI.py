from .version import VERSION
from robotlibcore import keyword

"""A library oor interaction with openshift using oc cli for robotframework
"""

_version_ = VERSION


class OpenShiftCLI(object):
    """
     This Test library provides keywords to work with openshift
      and various helper methods to check pod, service and related
      functionality via RobotFramework
    """
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    ROBOT_LIBRARY_VERSION = VERSION
    
    @keyword
    def get_pods(self, namespace: str='')->None:
        """
        Get the Pods specified in the namespace 
        default is all namespace
        """
        pass
    
    @keyword
    def get_pods_starting_with_name(self, startnames: str ='', namespace: str='')->None:
        """
        Get pods starting with name startname

        Args:
          startname: starting name of the pod eg: jupyterhub-db
          namespace: namespace

        Returns:
          output(Array): Values of pod names with array
        """
        pass
    
    @keyword
    def download_client(self)->None:
        pass
    
    @keyword
    def wait_for_pod_state(self, podname: str, state: str)->None:
        """
        """
        pass

    @keyword
    def check_pod_exists(self, podname: str, namespace:str)->None:
        pass
    
    @keyword
    def switch_project(self, project: str)->None:
        """
        Switch the project to projectname
        """
        pass
    
    @keyword
    def apply_yaml(self)->None:
        pass

    @keyword
    def upgrade_build(self)->None:
        pass
    
    @keyword
    def get_current_build(self)->None:
        pass
