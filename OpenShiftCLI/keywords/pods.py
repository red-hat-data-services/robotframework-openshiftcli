from kubernetes import config
from openshift.dynamic import DynamicClient
from robotlibcore import keyword
from robot.api import logger, Error
from typing import List, Dict
import time


class PodKeywords(object):
    def __init__(self) -> None:
        self.k8s_client = config.new_client_from_config()
        self.dyn_client = DynamicClient(self.k8s_client)
        self.v1_pods = self.dyn_client.resources.get(api_version='v1', kind='Pod')

    @keyword
    def get_pods(self, namespace: str = '') -> List[Dict[str, str]]:
        """
        Get the Pods specified in the namespace
        default is all namespace
        Args:
          Namespace: str

        Returns:
          output(List): Values of project names in a List

        """
        pod_list = self.v1_pods.get(namespace=namespace).items
        if not pod_list:
            logger.error(f'Pods not found in {namespace}')
            raise Error(f'Pods not found in {namespace}')
        pods = [{"name": pod.metadata.name, "status": pod.status.phase} for pod in pod_list]
        logger.info(pods)
        return pods

    @keyword
    def pods_should_contain(self, podname: str, namespace: str = "") -> List[Dict[str, str]]:
        """
        Get pods starting with name podname

        Args:
          podname: starting name of the pod eg: jupyterhub-db
          namespace: namespace

        Returns:
          output(List): Values of pod names and status with List
        """
        pod_list = self.v1_pods.get(namespace=namespace)
        pod_found = [{"name": pod.metadata.name, "status": pod.status.phase}
                     for pod in pod_list.items if (pod.metadata.name).startswith(podname)]
        logger.info(pod_found)
        if not pod_found:
            logger.error(f'Pod {podname} not found in namespace {namespace}')
            raise Error(
                f'Pod {podname} not found in namespace {namespace}'
            )
        return pod_found

    @keyword
    def wait_until_pods_available(self, namespace: str = '', timeout: int = 900) -> None:
        """
        Wait until pods are available

        Args:
          namespace: namespace
          timeout: timeout

        Returns:
          output: None
        """
        timer = time.time() + timeout
        while True:
            pods = self.v1_pods.get(namespace=namespace).items

            if all(pod.status.phase != "Pending" for pod in pods) and pods != []:
                if any(pod.status.phase != "Succeeded" and pod.status.phase != "Running" for pod in pods):
                    for pod in pods:
                        if pod.status.phase == "Failed":
                            logger.error(
                                f"""Error in pod {pod.metadata.name}\n
                                Status: {pod.status.phase}\n
                                Reason: {pod.status.reason}\n
                                Message: {pod.status.message}""")
                            raise Error(
                                f"""Error in pod {pod.metadata.name}\n
                                Status: {pod.status.phase}\n
                                Reason: {pod.status.reason}\n
                                Message: {pod.status.message}""")
                        elif pod.status.phase == "Unknown":
                            logger.info("unknown")
                            logger.error(
                                f"""Error in pod {pod.metadata.name}\n
                                Status: {pod.status.phase}\n
                                Reason: {pod.status.reason}\n
                                Message: {pod.status.message}""")
                            raise Error(
                                f"""Error in pod {pod.metadata.name}\n
                                Status: {pod.status.phase}\n
                                Reason: {pod.status.reason}\n
                                Message: {pod.status.message}""")
                        else:
                            logger.info(f"""Other status: {pod.metadata.name}\n
                            Status: {pod.status.phase}\n""")
                else:
                    logger.info(f'Pods: {self.get_pods(namespace)}')
                    break
            else:
                if time.time() > timer:
                    logger.warn(f'Timeout - pods: {self.get_pods(namespace)}')
                    break
                time.sleep(2)
