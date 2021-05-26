import shlex
import subprocess

from .version import VERSION
from robot.api import logger

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

    def __init__(self):
        self.oc_path = None
        self.oc_exec = None

    def oc_run_command(self, cmd, timeout=45, ignore_errors=False, **kwargs):
        """
        run oc command and get the output
        to set default namespace use default_namespace arg

        Args:
          default_namespace: default namspace to use for all operations

        Returns:
           output of the oc command: String
        """
        if self.oc_path is not None:
            oc = self.oc_path + '/oc'
        else:
            oc = 'oc'

        cmd = oc + ' ' + cmd
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)

        completed_process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            timeout=timeout,
            **kwargs,
        )
        logger.info(completed_process.stdout)
        return completed_process.stdout

    def oc_get_pods(self, namespace='-A'):
        """
        Get the Pods specified in the namespace 
        default is all namespace
        """
        return self.oc_run_command(cmd=f'get pods -n {namespace}')

    def oc_get_pods_starting_with_name(self, startnames='', namespace=''):
        """
        Get pods starting with name startname

        Args:
          startname: starting name of the pod eg: jupyterhub-db
          namespace: namespace

        Returns:
          output(Array): Values of pod names with array
        """
        out = self.oc_run_command(cmd=f'get pods {namespace} -o custom-columns="name:.metadata.name"')
        output = []
        for line in out:
            if line.startswith(startnames):
                output.append(line)
        return output

    def oc_download_client(self):
        pass

    def oc_wait_for_pod_state(self, podname, state):
        """
        """
        pass

    def oc_check_pod_exists(self, podname, namespace):
        pass

    def oc_switch_project(self, project):
        """
        Switch the project to projectname
        """
        self.oc_run_command(cmd=f'new-project {project}')

    def oc_apply_yaml(self):
        pass

    def oc_upgrade_build(self):
        pass

    def oc_get_current_build(self):
        pass
