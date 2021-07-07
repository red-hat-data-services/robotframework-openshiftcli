*** Settings ***
Documentation     ODS Test Library.
Library      OpenShiftCLI

*** Test Cases ***
Verify Project Keywords
  Get Projects
  Projects Should Contain  redhat-ods-applications

Verify Pods Keywords
  Get Pods  redhat-ods-applications
  Pods Should Contain  jupyterhub-db
  Wait Until Pods Available  namespace=redhat-ods-applications
  
Verify Service Keywords
  Get Services  redhat-ods-applications
  Services Should Contain  odh-dashboard  namespace=redhat-ods-applications