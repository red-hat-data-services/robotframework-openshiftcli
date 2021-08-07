from robotlibcore import DynamicCore
from OpenShiftCLI.keywords import (
    ClusterroleKeywords,
    ClusterrolebindingKeywords,
    ConfigmapKeywords,
    CRDKeywords,
    GroupKeywords,
    KFDEFKeywords,
    ListKeywords,
    PodKeywords,
    ProjectKeywords,
    RolebindingKeywords,
    SecretKeywords,
    ServiceKeywords,
)
from .apiclient import Apiclient
from .logstreamer import LogStreamer
from .plaintextformatter import PlaintextFormatter
from .version import VERSION

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
__version__ = VERSION


class OpenShiftCLI(DynamicCore):
    """
     This Test library provides keywords to work with openshift
      and various helper methods to check pod, service and rfrom .version import VERSIONelated
      functionality via RobotFramework
    """
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self) -> None:
        libraries = [
            ClusterroleKeywords(Apiclient('rbac.authorization.k8s.io/v1', 'ClusterRole')),
            ClusterrolebindingKeywords(Apiclient('rbac.authorization.k8s.io/v1', 'ClusterRoleBinding')),
            ConfigmapKeywords(Apiclient('v1', 'ConfigMap')),
            CRDKeywords(Apiclient('apiextensions.k8s.io/v1', 'CustomResourceDefinition')),
            GroupKeywords(Apiclient('user.openshift.io/v1', 'Group')),
            KFDEFKeywords(Apiclient('kfdef.apps.kubeflow.org/v1', 'KfDef')),
            ListKeywords(Apiclient('v1', 'List')),
            PodKeywords(Apiclient('v1', 'Pod'), PlaintextFormatter(), LogStreamer()),
            ProjectKeywords(Apiclient('project.openshift.io/v1', 'Project')),
            RolebindingKeywords(Apiclient('rbac.authorization.k8s.io/v1', 'RoleBinding')),
            SecretKeywords(Apiclient('v1', 'Secret')),
            ServiceKeywords(Apiclient('v1', 'Service'))]
        DynamicCore.__init__(self, libraries)
