*** Settings ***
Documentation     OpenShiftCLI Library
Library      OpenShiftCLI

*** Test Cases ***
Test Generic Keywords Kind Service
  New Project  test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
  ...  Get  kind=Service  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Create failed\nReason: Src required
  ...  Create  kind=Service  namespace=test-services
  Create  kind=Service  src=https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/service.yaml?ref\=/master  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Create failed\nReason: Src is not a valid path, url, yaml or json
  ...  Create  kind=Service  src=test-data/srvices.yaml  namespace=test-services
  Create  kind=Service  src=test-data/services.yaml  namespace=test-services
  Run Keyword And Expect Error   ResourceOperationFailed: Apply failed\nReason: Namespace is required for v1.Service	
  ...  Apply  Service  test-data/service_apply_create.yaml
  Apply  Service  test-data/service_apply_create.yaml  test-services
  Create  kind=Service  src=test-data/service_create.yaml  namespace=test-services
  Apply  kind=Service  src=test-data/service_apply.yaml  namespace=test-services
  Create  kind=Service  src=test-data/service_delete.yaml  namespace=test-services
  Get  kind=Service  namespace=test-services
  Get  Service
  Get  kind=Service
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Get failed\nReason: 404\nReason: Not Found
  ...  Get  Service  test-services 
  Get  kind=Service  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
  ...  Get  kind=Service  name=my-service-4  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
  ...  Get  Service  my-service-4  test-services
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Get failed\nReason: 404\nReason: Not Found
  ...  Get  kind=Service  name=my-service-4
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Get failed\nReason: 404\nReason: Not Found
  ...  Get  Service  my-service-4
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Get failed\nReason: 404\nReason: Not Found
  ...  Get  kind=Service  namespace=test-services  name=my-service-6
  Get  kind=Service  label_selector=environment=production  namespace=test-services
  Get  kind=Service  field_selector=metadata.name==my-service-4  namespace=test-services
  Patch  kind=Service  name=my-service-4  src={"spec": {"ports": [{"name": "https", "protocol": "TCP", "port": 443, "targetPort": 9377}]}}  namespace=test-services
  Patch  kind=Service  name=my-service-4  src={"metadata": {"labels": {"environment": "stage"}}}  namespace=test-services
  Patch  kind=Service  name=my-service-4  src={"metadata": {"labels": {"newlabel": "newvalue"}}}  namespace=test-services
  Watch  kind=Service  namespace=test-services 
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Watch failed\nReason: 404\nReason: Not Found
  ...  Watch  kind=Service  name=my-service-4
  Run Keyword And Expect Error  ResourceOperationFailed: Watch failed\nReason: Response is not chunked. Header 'transfer-encoding: chunked' is missing.
  ...  Watch  kind=Service  namespace=test-services  name=my-service-4
  Watch  kind=Service  namespace=test-services  label_selector=environment=stage
  Watch  kind=Service  namespace=test-services  field_selector=metadata.name==my-service-4
  Watch  kind=Service  namespace=test-services  resource_version=0
  Get  kind=Service  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Delete failed\nReason: Src or at least one of name, label_selector or field_selector is required
  ...  Delete  kind=Service
  Delete  kind=Service  src=https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/service.yaml?ref\=/master  namespace=test-services
  Delete  kind=Service  namespace=test-services  src=test-data/services.yaml
  Delete  kind=Service  src=test-data/service_apply_create.yaml  namespace=test-services
  Run Keyword And Expect Error  ResourceOperationFailed: Delete failed\nReason: At least one of namespace|label_selector|field_selector is required
  ...  Delete  kind=Service  src=test-data/service_apply.yaml
  Run Keyword And Expect Error  ResourceOperationFailed: Delete failed\nReason: Src or at least one of name, label_selector or field_selector is required, but not both
  ...  Delete  kind=Service  src=test-data/service_apply.yaml  name=my-service-4
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Delete failed\nReason: 404\nReason: Not Found
  ...  Delete  kind=Service  name=my-service-4  label_selector=environment=stage
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Delete failed\nReason: At least one of namespace|label_selector|field_selector is required
  ...  Delete  kind=Service  name=my-service-4
  Delete  kind=Service  name=my-service-4  namespace=test-services  label_selector=environment=stage 
  Delete  kind=Service  name=my-service-5  namespace=test-services 
  Watch  kind=Service  namespace=test-services  timeout=120
  Delete Project  test-services