from .version import VERSION
from robotlibcore import DynamicCore
from OpenShiftCLI.keywords import (
    ListKeywords,
    PodKeywords,
    ProjectKeywords,
    SecretKeywords,
    ServiceKeywords,
)
from .apiclient import Apiclient
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
__version__ = VERSION


class OpenShiftCLI(DynamicCore):
    """
     This Test library provides keywords to work with openshift
      and various helper methods to check pod, service and related
      functionality via RobotFramework
    """
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self) -> None:
        libraries = [ListKeywords(Apiclient('v1', 'List')),
                     PodKeywords(Apiclient('v1', 'Pod')),
                     ProjectKeywords(Apiclient('project.openshift.io/v1', 'Project')),
                     SecretKeywords(Apiclient('v1', 'Secret')),
                     ServiceKeywords(Apiclient('v1', 'Service'))]
        DynamicCore.__init__(self, libraries)
