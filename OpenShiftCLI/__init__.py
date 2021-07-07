from .version import VERSION
from robotlibcore import DynamicCore
from OpenShiftCLI.keywords import (
    PodKeywords,
    ProjectKeywords,
    ServiceKeywords,
)

_version_ = VERSION


class OpenShiftCLI(DynamicCore):
    """
     This Test library provides keywords to work with openshift
      and various helper methods to check pod, service and related
      functionality via RobotFramework
    """
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self) -> None:
        libraries = [PodKeywords(), ProjectKeywords(), ServiceKeywords()]
        DynamicCore.__init__(self, libraries)
