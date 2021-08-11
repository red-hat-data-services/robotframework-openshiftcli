*** Settings ***
Documentation     OpenShiftCLI Library.
Library      OpenShiftCLI

*** Test Cases ***
Test Project Keywords
  New Project  test-projects
  Wait Until Project Exists  test-projects
  Projects Should Contain  test-projects
  Apply Project  test-data/project.yaml
  Delete Project  test-projects
  Delete Project  my-project
  Get Projects

Test Service Keywords
  New Project  test-services
  Create Service  test-data/service.yaml  namespace=test-services
  Services Should Contain  my-service  namespace=test-services
  Get Services  namespace=test-services
  Delete Service  my-service  namespace=test-services
  Delete Project  test-services

Test Secret Keywords
  New Project  test-secrets
  Create Secret  test-data/secret.yaml  namespace=test-secrets
  Apply Secret  test-data/secret_apply.yaml  namespace=test-secrets
  Delete Secret  my-secret  namespace=test-secrets
  Delete Secret From File  test-data/secret_apply.yaml
  Delete Project  test-secrets

Test ConfigMap Keywords
  New Project  test-configmaps
  Create ConfigMap  test-data/configmap.yaml  namespace=test-configmaps
  Delete ConfigMap  my-configmap  namespace=test-configmaps
  Delete Project  test-configmaps

Test Group Keywords
  Create Group  test-data/group.yaml
  Delete Group  my-group

Test List Keywords
  New Project  test-lists
  Create Objects List  test-data/list.yaml  namespace=test-lists
  Apply Objects List  test-data/list_apply.yaml  namespace=test-lists
  Delete Project  test-lists

Test Custom Resource Definition Keywords
  New Project  test-crd
  Create CRD  test-data/crd.yaml  namespace=test-crd
  Delete CRD  crontabs.stable.example.com
  Delete Project  test-crd

Test User, Role and Role Binding Keywords
  New Project  test-roles
  Create User  test-data/user.yaml
  Create Role  test-data/role.yaml
  Create Role Binding  test-data/rolebinding.yaml
  Delete Role Binding  read-pods  namespace=test-roles
  Delete Role  pod-reader  namespace=test-roles
  Delete User  Pablo
  Delete Project  test-roles

Test User, Cluster Role and Cluster Role Binding Keywords
  New Project  test-clusterroles
  Create User  test-data/user.yaml
  Create Cluster Role  test-data/clusterrole.yaml
  Create Cluster Role Binding  test-data/clusterrolebinding.yaml
  Delete Cluster Role Binding  read-secrets-global
  Delete Cluster Role  secret-reader
  Delete User  Pablo
  Delete Project  test-clusterroles

Test Kfdef Keywords
  New Project  test-kfdefs
  Create Kfdef  test-data/kfdef.yaml  namespace=test-kfdefs
  Delete Kfdef  test   namespace=test-kfdefs
  Delete Project  test-kfdefs

Test Pods Keywords
  New Project  test-pods
  Create Pod  test-data/pod.yaml  namespace=test-pods
  Wait For Pods Number  1  namespace=test-pods
  wait For Pods Status  namespace=test-pods
  Get Pods  namespace=test-pods
  Delete Pod  my-pod  namespace=test-pods
  Search Pods  my  namespace=test-pods  label_selector=role=myrole
  Delete Project  test-pods
