*** Settings ***
Documentation     OpenShiftCLI Library
Library      OpenShiftCLI

*** Test Cases ***
Test Template 1
  @{list} =  Apply  Pod  test-data/template.yaml  namespace=default  template_data={image: nginx, name: web}
  &{dictionary} =  Set Variable  ${list}[0]
  Delete  kind=Pod  name=${dictionary.metadata.name}  namespace=default

Test Template 2
  @{list} =  Apply  Pod  test-data/template.yaml  namespace=default  template_data={"image": "nginx", "name": "nginx"}
  &{dictionary} =  Set Variable  ${list}[0]
  Delete  kind=Pod  name=${dictionary.metadata.name}  namespace=default

Test Template 3
  @{list} =  Apply  Pod  test-data/template.yaml  namespace=default  template_data={'image': 'nginx', 'name': 'my-app'}
  &{dictionary} =  Set Variable  ${list}[0]
  Delete  kind=Pod  name=${dictionary.metadata.name}  namespace=default

Test Template 4
  @{list} =  Apply  Pod  test-data/template.yaml  namespace=default  template_data={image: 'nginx', name: 'server'}
  &{dictionary} =  Set Variable  ${list}[0]
  Delete  kind=Pod  name=${dictionary.metadata.name}  namespace=default

Test Template 5
  Run Keyword And Expect Error  STARTS: ResourceOperationFailed: Apply failed\nReason: Load data from jinja failed\nwhile parsing a block mapping
  ...  Apply  Pod  test-data/template.yaml  namespace=default  template_data=image: 'nginx', name: 'web'}

Test Template 6
  &{template_data} =  Create Dictionary   image=nginx  name=web
  @{list} =  Apply  Pod  test-data/template.yaml  namespace=default  template_data=${template_data}
  &{dictionary} =  Set Variable  ${list}[0]
  Delete  kind=Pod  name=${dictionary.metadata.name}  namespace=default