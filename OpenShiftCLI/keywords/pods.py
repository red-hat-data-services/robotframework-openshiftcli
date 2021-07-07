from kubernetes import config
from openshift.dynamic import DynamicClient
from robotlibcore import keyword
from robot.api import logger
from typing import List, Dict


class PodKeywords(object):

    k8s_client = config.new_client_from_config()
    dyn_client = DynamicClient(k8s_client)
    v1_pods = dyn_client.resources.get(api_version='v1', kind='Pod')

    @keyword
    def get_pods(self, namespace: str = '') -> List[str]:
        """
        Get the Pods specified in the namespace 
        default is all namespace
        """
        pod_list = self.v1_pods.get(namespace=namespace)
        pods = [pod.metadata.name for pod in pod_list.items]
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
        pod_found = [{pod.metadata.name: pod.status.phase}
                     for pod in pod_list.items if (pod.metadata.name).startswith(podname)]
        logger.info(pod_found)
        return pod_found

    @keyword
    def wait_until_pods_available(self, namespace: str = '', timeout: str = 2) -> None:
        pods = self.v1_pods.watch(namespace=namespace, timeout=timeout)
        for event in pods:
            logger.info(f'{event["object"].metadata.name}\nStatus:{event["object"].status.phase}')
            if event['object'].status.phase == 'Failed':
                logger.error(
                    f'Error in pod {event["object"].metadata.name}\nStatus: {event["object"].status.phase}\nReason: {event["object"].status.reason}\nMessage: {event["object"].status.message}')
                raise Exception(
                    f'Error in pod {event["object"].metadata.name}\nStatus: {event["object"].status.phase}\nReason: {event["object"].status.reason}\nMessage: {event["object"].status.message}')
