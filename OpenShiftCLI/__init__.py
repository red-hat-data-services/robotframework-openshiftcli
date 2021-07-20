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
        libraries = [ListKeywords(),
                     PodKeywords(),
                     ProjectKeywords(Apiclient('project.openshift.io/v1', 'Project')),
                     SecretKeywords(),
                     ServiceKeywords()]
        DynamicCore.__init__(self, libraries)
