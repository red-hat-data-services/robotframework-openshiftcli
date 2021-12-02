*** Settings ***
Documentation     OpenShiftCLI Library
Library      OpenShiftCLI

*** Test Cases ***
Test Generic Keywords Kind Service
  New Project  test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
  ...  Oc Get  kind=Service  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Create failed\nReason: Namespace is required for v1.Service 
  ...  Oc Create  kind=Service  src=test-data/service.yaml
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Create failed\nReason: 400\nReason: Bad Request
  ...  Oc Create  kind=Service  src=test-data/srvice.yaml  namespace=test-services
  Oc Create  kind=Service  src=https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/service.yaml?ref\=/master  namespace=test-services
  Oc Create  kind=Service  src=test-data/services.yaml  namespace=test-services
  Run Keyword And Expect Error   AttributeError: 'str' object has no attribute 'get'	
  ...  Oc Apply  Service  test-data/service_apply_creat.yaml
  Run Keyword And Expect Error   ResourceOperationFailed: Apply failed\nReason: Namespace is required for v1.Service	
  ...  Oc Apply  Service  test-data/service_apply_create.yaml
  Oc Apply  Service  test-data/service_apply_create.yaml  test-services
  Oc Create  kind=Service  src=test-data/service_create.yaml  namespace=test-services
  Oc Apply  kind=Service  src=test-data/service_apply.yaml  namespace=test-services
  Oc Create  kind=Service  src=test-data/service_delete.yaml  namespace=test-services
  Oc Get  kind=Service  namespace=test-services
  Oc Get  Service
  Oc Get  kind=Service
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Get failed\nReason: 404\nReason: Not Found
  ...  Oc Get  Service  test-services 
  Oc Get  kind=Service  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
  ...  Oc Get  kind=Service  name=my-service-4  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
  ...  Oc Get  Service  my-service-4  test-services
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Get failed\nReason: 404\nReason: Not Found
  ...  Oc Get  kind=Service  name=my-service-4
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Get failed\nReason: 404\nReason: Not Found
  ...  Oc Get  Service  my-service-4
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Get failed\nReason: 404\nReason: Not Found
  ...  Oc Get  kind=Service  namespace=test-services  name=my-service-6
  Oc Get  kind=Service  label_selector=environment=production  namespace=test-services
  Oc Get  kind=Service  field_selector=metadata.name==my-service-4  namespace=test-services
  Oc Patch  kind=Service  name=my-service-4  src={"spec": {"ports": [{"name": "https", "protocol": "TCP", "port": 443, "targetPort": 9377}]}}  namespace=test-services
  Oc Patch  kind=Service  name=my-service-4  src={"metadata": {"labels": {"environment": "stage"}}}  namespace=test-services
  Oc Patch  kind=Service  name=my-service-4  src={"metadata": {"labels": {"newlabel": "newvalue"}}}  namespace=test-services
  Oc Watch  kind=Service  namespace=test-services 
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Watch failed\nReason: 404\nReason: Not Found
  ...  Oc Watch  kind=Service  name=my-service-4
  Run Keyword And Expect Error  ResourceOperationFailed: Watch failed\nReason: Response is not chunked. Header 'transfer-encoding: chunked' is missing.
  ...  Oc Watch  kind=Service  namespace=test-services  name=my-service-4
  Oc Watch  kind=Service  namespace=test-services  label_selector=environment=stage
  Oc Watch  kind=Service  namespace=test-services  field_selector=metadata.name==my-service-4
  Oc Watch  kind=Service  namespace=test-services  resource_version=0
  Oc Get  kind=Service  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Delete failed\nReason: Src or at least one of name, label_selector or field_selector is required
  ...  Oc Delete  kind=Service
  Oc Delete  kind=Service  src=https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/service.yaml?ref\=/master  namespace=test-services
  Oc Delete  kind=Service  namespace=test-services  src=test-data/services.yaml
  Oc Delete  kind=Service  src=test-data/service_apply_create.yaml  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Delete failed\nReason: At least one of namespace|label_selector|field_selector is required
  ...  Oc Delete  kind=Service  src=test-data/service_apply.yaml
  Run Keyword And Expect Error  ResourceOperationFailed: Delete failed\nReason: Src or at least one of name, label_selector or field_selector is required, but not both
  ...  Oc Delete  kind=Service  src=test-data/service_apply.yaml  name=my-service-4
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Delete failed\nReason: 404\nReason: Not Found
  ...  Oc Delete  kind=Service  name=my-service-4  label_selector=environment=stage
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Delete failed\nReason: At least one of namespace|label_selector|field_selector is required
  ...  Oc Delete  kind=Service  name=my-service-4
  Oc Delete  kind=Service  name=my-service-4  namespace=test-services  label_selector=environment=stage 
  Oc Delete  kind=Service  name=my-service-5  namespace=test-services 
  Oc Watch  kind=Service  namespace=test-services  timeout=120
  Oc Delete  kind=Project  name=test-services