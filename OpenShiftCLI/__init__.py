import urllib3

from robotlibcore import DynamicCore

from OpenShiftCLI.keywords import (
    ClusterrolebindingKeywords,
    ClusterroleKeywords,
    ConfigmapKeywords,
    CRDKeywords,
    GroupKeywords,
    KFDEFKeywords,
    ListKeywords,
    PodKeywords,
    ProjectKeywords,
    RoleKeywords,
    RolebindingKeywords,
    SecretKeywords,
    ServiceKeywords,
    UserKeywords
)
from OpenShiftCLI.cliclient import ApiClient
from OpenShiftCLI.dataloader import DataLoader
from OpenShiftCLI.dataparser import DataParser
from OpenShiftCLI.outputstreamer import LogStreamer
from OpenShiftCLI.outputformatter import PlaintextFormatter


from .version import VERSION


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
__version__ = VERSION


class OpenShiftCLI(DynamicCore):
    """
     This Test library provides keywords to work with openshift
      and various helper methods to check pod, service and rfrom .version import VERSIONelated
      functionality via RobotFramework
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self) -> None:
        libraries = [
            ClusterrolebindingKeywords(
                ApiClient('rbac.authorization.k8s.io/v1', 'ClusterRoleBinding'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            ClusterroleKeywords(
                ApiClient('rbac.authorization.k8s.io/v1', 'ClusterRole'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            ConfigmapKeywords(
                ApiClient('v1', 'ConfigMap'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            CRDKeywords(
                ApiClient('apiextensions.k8s.io/v1', 'CustomResourceDefinition'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            GroupKeywords(
                ApiClient('user.openshift.io/v1', 'Group'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()),
            KFDEFKeywords(
                ApiClient('kfdef.apps.kubeflow.org/v1', 'KfDef'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            ListKeywords(
                ApiClient('v1', 'List'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            PodKeywords(
                ApiClient('v1', 'Pod'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            ProjectKeywords(
                ApiClient('project.openshift.io/v1', 'Project'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            RoleKeywords(
                ApiClient('rbac.authorization.k8s.io/v1', 'Role'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            RolebindingKeywords(
                ApiClient('rbac.authorization.k8s.io/v1', 'RoleBinding'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            SecretKeywords(
                ApiClient('v1', 'Secret'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            ServiceKeywords(
                ApiClient('v1', 'Service'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            ),
            UserKeywords(
                ApiClient('user.openshift.io/v1', 'User'),
                DataLoader(),
                DataParser(),
                PlaintextFormatter(),
                LogStreamer()
            )]
        DynamicCore.__init__(self, libraries)
