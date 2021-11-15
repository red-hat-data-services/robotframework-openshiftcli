*** Settings ***
Documentation     OpenShiftCLI Library
Library      OpenShiftCLI

*** Test Cases ***
Test keywords return values
    New Project  test-services
    Create  kind=Service  src=test-data/service.yaml  namespace=test-services
    @{list} =  Get  kind=Service  field_selector=metadata.name==my-service
    Log   ${list}[0]
    Apply  Service  ${list}[0]  test-services
    &{dictionary} =  Set Variable  ${list}[0]
    Log  ${dictionary.metadata.name}
    Patch  kind=Service  name=${dictionary.metadata.name}  src={"metadata": {"labels": {"environment": "production"}}}  namespace=test-services
    Delete  kind=Service  name=my-service  namespace=test-services
    Delete Project  test-services
    