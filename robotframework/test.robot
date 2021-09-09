*** Settings ***
Documentation     OpenShiftCLI Library.
Library      OpenShiftCLI

*** Test Cases ***
Test Project Keywords
  New Project  test-projects
  Wait Until Project Exists  test-projects
  Get Projects
  Projects Should Contain  test-projects
  Delete Project  test-projects
  Wait Until Project Does Not Exists  test-projects  timeout=10


 Test Service Keywords
   New Project  test-services
   Create Service  https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/service.yaml?ref\=/feature/templates  namespace=test-services
   Create Service  test-data/services.yaml  namespace=test-services
   Get Services  namespace=test-services
   Services Should Contain  my-service  namespace=test-services
   Delete Service  my-service  namespace=test-services
   Delete Service  my-service-1  namespace=test-services
   Delete Service  my-service-2  namespace=test-services
   Delete Project  test-services

Test Secret Keywords
  New Project  test-secrets
  Create Secret  test-data/secret.yaml  namespace=test-secrets
  Create Secret  test-data/secrets.yaml  namespace=test-secrets
  Apply Secret  https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/secret.yaml?ref\=/feature/templates  namespace=test-secrets
  Run Keyword And Expect Error  Content was not found. Verify url https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/secreto.yaml?ref\=/feature/templates is correct
  ...  Apply Secret  https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/secreto.yaml?ref\=/feature/templates  namespace=test-secrets
  Apply Secret  test-data/secret_apply.yaml  namespace=test-secrets
  Delete Secret  my-secret  namespace=test-secrets
  Delete Secret From File  test-data/secrets.yaml  namespace=test-secrets
  Delete Secret From File  test-data/secret_apply.yaml
  Delete Project  test-secrets

Test ConfigMap Keywords
  New Project  test-configmaps
  Create ConfigMap  test-data/configmap.yaml  namespace=test-configmaps
  Create ConfigMap  test-data/configmaps.yaml  namespace=test-configmaps
  Patch ConfigMap  my-configmap  body={"data": {"player_initial_lives": "4"}}  namespace=test-configmaps
  Delete Configmap From File  test-data/configmaps.yaml  namespace=test-configmaps
  Delete ConfigMap  my-configmap  namespace=test-configmaps
  Delete Project  test-configmaps

Test Group Keywords
  Create Group  test-data/group.yaml
  Delete Group  my-group

Test List Keywords
  New Project  test-lists
  Create Resources List  test-data/list.yaml  namespace=test-lists
  Apply Resources List  test-data/list_apply.yaml  namespace=test-lists
  Delete Resources List  test-data/list.yaml  namespace=test-lists
  Delete Project  test-lists

Test Custom Resource Definition Keywords
  New Project  test-crds
  Create CRD  test-data/crd.yaml  namespace=test-crds
  Delete CRD  crontabs.stable.example.com
  Delete Project  test-crds

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
  Get Kfdefs  namespace=test-kfdefs
  Patch Kfdef  test  body={"metadata": {"finalizers": []}}  namespace=test-kfdefs
  Sleep  10
  Delete Kfdef  test   namespace=test-kfdefs
  Delete Project  test-kfdefs

Test Pods Keywords
  New Project  test-pods
  Create Pod  test-data/pod.yaml  namespace=test-pods
  Create Pod  test-data/pods.yaml  namespace=test-pods
  Wait For Pods Number  1  namespace=test-pods
  Wait For Pods Status  namespace=test-pods
  Get Pods  namespace=test-pods
  Search Pods  my  namespace=test-pods  label_selector=role=myrole
  Delete Pod  my-pod  namespace=test-pods
  Delete Pod  my-pod-1  namespace=test-pods
  Delete Pod  my-pod-2  namespace=test-pods
  Delete Project  test-pods
