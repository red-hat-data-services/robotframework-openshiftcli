*** Settings ***
Documentation     openshiftcli Library
Library      openshiftcli

*** Test Cases ***
Test keywords return values
    New Project  test-services
    Oc Create  kind=Service  src=test-data/service.yaml  namespace=test-services
    @{list} =  Oc Get  kind=Service  field_selector=metadata.name==my-service
    Log   ${list}[0]
    Oc Apply  Service  ${list}[0]  test-services
    &{dictionary} =  Set Variable  ${list}[0]
    Log  ${dictionary.metadata.name}
    Oc Patch  kind=Service  name=${dictionary.metadata.name}  src={"metadata": {"labels": {"environment": "production"}}}  namespace=test-services
    Oc Delete  kind=Service  name=my-service  namespace=test-services
    Oc Delete  kind=Project  name=test-services
    