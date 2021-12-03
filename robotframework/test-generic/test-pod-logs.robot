*** Settings ***
Documentation     OpenShiftCLI Library
Library      OpenShiftCLI

*** Test Cases ***
Test keyword Get Pod Logs
  New Project  test-pod-logs
  Oc Create  kind=Pod  src=test-data/pod.yaml  namespace=test-pod-logs
  Sleep  20
  Oc Get Pod Logs  name=my-pod  namespace=test-pod-logs
  Oc Delete  kind=Pod  name=my-pod  namespace=test-pod-logs
  Oc Delete  kind=Project  name=test-pod-logs