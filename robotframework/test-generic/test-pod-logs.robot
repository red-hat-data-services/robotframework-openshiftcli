*** Settings ***
Documentation     OpenShiftCLI Library
Library      OpenShiftCLI

*** Test Cases ***
Test keyword Get Pod Logs
  New Project  test-pod-logs
  Create  kind=Pod  src=test-data/pod.yaml  namespace=test-pod-logs
  Sleep  20
  Get Pod Logs  name=my-pod  namespace=test-pod-logs
  Delete  kind=Pod  name=my-pod  namespace=test-pod-logs
  Delete Project  test-pod-logs