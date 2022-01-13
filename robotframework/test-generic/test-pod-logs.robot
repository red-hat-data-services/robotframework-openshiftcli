*** Settings ***
Documentation     openshiftcli Library
Library      openshiftcli

*** Test Cases ***

Test keyword Get Pod Logs
  New Project  test-pod-logs
  Oc Create  kind=Pod  src=test-data/pod_with_containers.yaml  namespace=test-pod-logs
  Sleep  20
  Oc Get Pod Logs  name=my-pod  namespace=test-pod-logs  container=web
  Oc Get Pod Logs  name=my-pod  namespace=test-pod-logs  timestamps=true  tailLines=2  container=web
  Oc Get Pod Logs  name=my-pod  namespace=test-pod-logs  timestamps=true  container=second-web
  Oc Delete  kind=Pod  name=my-pod  namespace=test-pod-logs
  Oc Delete  kind=Project  name=test-pod-logs