*** Settings ***
Documentation     OpenShiftCLI Library
Library      OpenShiftCLI

*** Test Cases ***
Test Generic Keywords Kind Project
  New Project  test-projects
  Get  kind=Project
  Get  kind=Project  field_selector=metadata.name==test-projects
  Get  kind=Project  field_selector=metadata.name==rhods-notebooks
  Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
  ...  Get  kind=Project  name=test-projects
  Get  kind=Project  namespace=test-projects
  Delete  kind=Project  name=test-projects

Test Generic Keywords Kind Deployment
   New Project  test-deployments
   Create   kind=Deployment  src=test-data/deployment.yaml  namespace=test-deployments
   Get  kind=Deployment  field_selector=metadata.name==my-deployment  namespace=test-deployments
   Apply  kind=Deployment  src=test-data/deployment_apply.yaml  namespace=test-deployments
   Get  kind=Deployment  field_selector=metadata.name==my-deployment  namespace=test-deployments
   Patch  kind=Deployment  name=my-deployment  src={"spec": {"progressDeadlineSeconds":400}}  namespace=test-deployments
   Get  kind=Deployment  field_selector=metadata.name==my-deployment  namespace=test-deployments
   Delete  kind=Deployment  name=my-deployment  namespace=test-deployments
   Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
   ...  Get  kind=Deployment  field_selector=metadata.name==my-deployment  namespace=test-deployments
   Delete Project  test-deployments

Test Generic Keywords Kind List
  New Project  test-lists
  Run Keyword And Expect Error  ResourceOperationFailed: Create failed\nReason: string indices must be integers    
  ...  Create  kind=List  src=test-data/lis.yaml  namespace=test-lists
  Create  kind=List  src=test-data/list.yaml  namespace=test-lists
  Apply   kind=List  src=test-data/list_apply.yaml  namespace=test-lists
  Delete  kind=List  src=test-data/list_apply.yaml  namespace=test-lists
  Delete  kind=List  src=test-data/list.yaml  namespace=test-lists
  Delete Project  test-lists

Test Generic Keywords Kind Secret
  New Project  test-secrets
  Create  kind=Secret  src=test-data/secret.yaml  namespace=test-secrets
  Create  kind=Secret  src=test-data/secrets.yaml  namespace=test-secrets
  Apply  kind=Secret  src=https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/secret.yaml?ref\=/master  namespace=test-secrets
  Run Keyword And Expect Error  ResourceOperationFailed: Apply failed\nReason: Load data from url failed\nContent was not found. Verify url https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/secreto.yaml?ref\=/feature/templates is correct
  ...  Apply  kind=Secret  src=https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/secreto.yaml?ref\=/feature/templates  namespace=test-secrets
  Apply  kind=Secret  src=test-data/secret_apply.yaml  namespace=test-secrets
  Delete  kind=Secret  name=my-secret  namespace=test-secrets
  Delete  kind=Secret  src=test-data/secrets.yaml  namespace=test-secrets
  Delete  kind=Secret  src=test-data/secret_apply.yaml
  Delete Project  test-secrets

Test Generic Keywords Kind ConfigMap
  New Project  test-configmaps
  Create  kind=ConfigMap  src=test-data/configmap.yaml  namespace=test-configmaps
  Create  kind=ConfigMap  src=test-data/configmaps.yaml  namespace=test-configmaps
  Patch  kind=ConfigMap  name=my-configmap  src={"data": {"player_initial_lives": "4"}}  namespace=test-configmaps
  Delete  kind=ConfigMap  src=test-data/configmaps.yaml  namespace=test-configmaps
  Delete  kind=ConfigMap  name=my-configmap  namespace=test-configmaps
  Delete Project  test-configmaps

Test Generic Keywords Kind Group
  Create  kind=Group  src=test-data/group.yaml
  Delete  kind=Group  name=my-group

Test Generic Keywords Kind CustomResourceDefinition
  New Project  test-crds
  Create  kind=CustomResourceDefinition  src=test-data/crd.yaml  namespace=test-crds
  Delete  kind=CustomResourceDefinition  name=crontabs.stable.example.com
  Delete Project  test-crds

Test Generic Keywords User, Role and RoleBinding 
  New Project  test-roles
  Create  kind=User  src=test-data/user.yaml
  Create  kind=Role  src=test-data/role.yaml
  Create  kind=RoleBinding  src=test-data/rolebinding.yaml
  Delete  kind=RoleBinding  name=read-pods  namespace=test-roles
  Delete  kind=Role  name=pod-reader  namespace=test-roles
  Delete  kind=User  name=Pablo
  Delete Project  test-roles

Test Generic Keywords Kind User, ClusterRole and ClusterRoleBinding
  New Project  test-clusterroles
  Create  kind=User  src=test-data/user.yaml
  Create  kind=ClusterRole  src=test-data/clusterrole.yaml
  Create  kind=ClusterRoleBinding  src=test-data/clusterrolebinding.yaml
  Delete  kind=ClusterRoleBinding  name=read-secrets-global
  Delete  kind=ClusterRole  name=secret-reader
  Delete  kind=User  name=Pablo
  Delete Project  test-clusterroles

Test Keywords KfDef
  New Project  test-kfdefs
  Create  kind=KfDef  src=test-data/kfdef.yaml  namespace=test-kfdefs
  Get  kind=KfDef  namespace=test-kfdefs
  Patch  kind=KfDef  name=test  src={"metadata": {"finalizers": []}}  namespace=test-kfdefs
  Sleep  10
  Delete  kind=KfDef  name=test   namespace=test-kfdefs
  Delete Project  test-kfdefs

Test Generic Keywords Kind Pod
  New Project  test-pods
  Create  kind=Pod  src=test-data/pod.yaml  namespace=test-pods
  Create  kind=Pod  src=test-data/pods.yaml  namespace=test-pods
  Get  kind=Pod  namespace=test-pods
  Delete  kind=Pod  name=my-pod  namespace=test-pods
  Delete  kind=Pod  name=my-pod-1  namespace=test-pods
  Delete  kind=Pod  name=my-pod-2  namespace=test-pods
  Delete Project  test-pods

Test Generic Keywords Kind Event
  New Project  test-events
  Get  kind=Event  namespace=redhat-ods-applications
  Delete Project  test-events



