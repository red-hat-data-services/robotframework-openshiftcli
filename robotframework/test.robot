*** Settings ***
Documentation     OpenShiftCLI Library.
Library      OpenShiftCLI

*** Test Cases ***
Verify Project Keywords
  New Project  test
  Delete Project  test
  Get Projects
  Projects Should Contain  default
