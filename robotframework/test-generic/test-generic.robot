*** Settings ***
Documentation     OpenShiftCLI Library
Library      OpenShiftCLI

*** Test Cases ***
Test Generic Keywords Kind Project
  New Project  test-projects
  Oc Get  kind=Project
  Oc Get  kind=Project  field_selector=metadata.name==test-projects
  Oc Get  kind=Project  field_selector=metadata.name==rhods-notebooks
  Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
  ...  Oc Get  kind=Project  name=test-projects
  Oc Get  kind=Project  namespace=test-projects
  Run Keyword And Expect Error  AttributeError: 'str' object has no attribute 'get'
  ...  Oc Delete  Project  test-projects
  Run Keyword And Expect Error  ResourceOperationFailed: Delete failed\nReason: Src or at least one of name, label_selector or field_selector is required, but not both 	
  ...  Oc Delete  Project  None  test-projects
  Oc Delete  kind=Project  name=test-projects

Test Generic Keywords Kind Deployment
   New Project  test-deployments
   Oc Create   kind=Deployment  src=test-data/deployment.yaml  namespace=test-deployments
   Oc Get  kind=Deployment  field_selector=metadata.name==my-deployment  namespace=test-deployments
   Oc Apply  kind=Deployment  src=test-data/deployment_apply.yaml  namespace=test-deployments
   Oc Get  kind=Deployment  field_selector=metadata.name==my-deployment  namespace=test-deployments
   Oc Patch  kind=Deployment  name=my-deployment  src={"spec": {"progressDeadlineSeconds":400}}  namespace=test-deployments
   Oc Get  kind=Deployment  field_selector=metadata.name==my-deployment  namespace=test-deployments
   Oc Delete  kind=Deployment  name=my-deployment  namespace=test-deployments
   Run Keyword And Expect Error  ResourceOperationFailed: Get failed\nReason: Not Found
   ...  Oc Get  kind=Deployment  field_selector=metadata.name==my-deployment  namespace=test-deployments
   Oc Delete  kind=Project  name=test-deployments

Test Generic Keywords Kind List
  New Project  test-lists
  Run Keyword And Expect Error  ResourceOperationFailed: Create failed\nReason: string indices must be integers    
  ...  Oc Create  kind=List  src=test-data/lis.yaml  namespace=test-lists
  Oc Create  kind=List  src=test-data/list.yaml  namespace=test-lists
  Oc Apply   kind=List  src=test-data/list_apply.yaml  namespace=test-lists
  Oc Delete  kind=List  src=test-data/list_apply.yaml  namespace=test-lists
  Oc Delete  kind=List  src=test-data/list.yaml  namespace=test-lists
  Oc Delete  kind=Project  name=test-lists

Test Generic Keywords Kind Secret
  New Project  test-secrets
  Oc Create  kind=Secret  src=test-data/secret.yaml  namespace=test-secrets
  Oc Create  kind=Secret  src=test-data/secrets.yaml  namespace=test-secrets
  Oc Apply  kind=Secret  src=https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/secret.yaml?ref\=/master  namespace=test-secrets
  Run Keyword And Expect Error  ResourceOperationFailed: Apply failed\nReason: Load data from url failed\nContent was not found. Verify url https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/secreto.yaml?ref\=/feature/templates is correct
  ...  Oc Apply  kind=Secret  src=https://api.github.com/repos/pablofelix/robotframework-OpenShiftCLI/contents/test-data/secreto.yaml?ref\=/feature/templates  namespace=test-secrets
  Oc Apply  kind=Secret  src=test-data/secret_apply.yaml  namespace=test-secrets
  Oc Delete  kind=Secret  name=my-secret  namespace=test-secrets
  Oc Delete  kind=Secret  src=test-data/secrets.yaml  namespace=test-secrets
  Oc Delete  kind=Secret  src=test-data/secret_apply.yaml
  Oc Delete  kind=Project  name=test-secrets

Test Generic Keywords Kind ConfigMap
  New Project  test-configmaps
  Oc Create  kind=ConfigMap  src=test-data/configmap.yaml  namespace=test-configmaps
  Oc Create  kind=ConfigMap  src=test-data/configmaps.yaml  namespace=test-configmaps
  Oc Patch  kind=ConfigMap  name=my-configmap  src={"data": {"player_initial_lives": "4"}}  namespace=test-configmaps
  Oc Delete  kind=ConfigMap  src=test-data/configmaps.yaml  namespace=test-configmaps
  Oc Delete  kind=ConfigMap  name=my-configmap  namespace=test-configmaps
  Oc Delete  kind=Project  name=test-configmaps

Test Generic Keywords Kind Group
  Oc Create  kind=Group  src=test-data/group.yaml
  Oc Delete  kind=Group  name=my-group

Test Generic Keywords Kind CustomResourceDefinition
  New Project  test-crds
  Oc Create  kind=CustomResourceDefinition  src=test-data/crd.yaml  namespace=test-crds
  Oc Delete  kind=CustomResourceDefinition  name=crontabs.stable.example.com
  Oc Delete  kind=Project  name=test-crds

Test Generic Keywords User, Role and RoleBinding 
  New Project  test-roles
  Oc Create  kind=User  src=test-data/user.yaml
  Oc Create  kind=Role  src=test-data/role.yaml
  Oc Create  kind=RoleBinding  src=test-data/rolebinding.yaml
  Oc Delete  kind=RoleBinding  name=read-pods  namespace=test-roles
  Oc Delete  kind=Role  name=pod-reader  namespace=test-roles
  Oc Delete  kind=User  name=Pablo
  oc Delete  kind=Project  name=test-roles

Test Generic Keywords Kind User, ClusterRole and ClusterRoleBinding
  New Project  test-clusterroles
  Oc Create  kind=User  src=test-data/user.yaml
  Oc Create  kind=ClusterRole  src=test-data/clusterrole.yaml
  Oc Create  kind=ClusterRoleBinding  src=test-data/clusterrolebinding.yaml
  Oc Delete  kind=ClusterRoleBinding  name=read-secrets-global
  Oc Delete  kind=ClusterRole  name=secret-reader
  Oc Delete  kind=User  name=Pablo
  Oc Delete  kind=Project  name=test-clusterroles

Test Keywords KfDef
  New Project  test-kfdefs
  Oc Create  kind=KfDef  src=test-data/kfdef.yaml  namespace=test-kfdefs
  Oc Get  kind=KfDef  namespace=test-kfdefs
  Oc Patch  kind=KfDef  name=test  src={"metadata": {"finalizers": []}}  namespace=test-kfdefs
  Sleep  10
  Oc Delete  kind=KfDef  name=test   namespace=test-kfdefs
  Oc Delete  kind=Project  name=test-kfdefs

Test Generic Keywords Kind Pod
  New Project  test-pods
  Oc Create  kind=Pod  src=test-data/pod.yaml  namespace=test-pods
  Oc Create  kind=Pod  src=test-data/pods.yaml  namespace=test-pods
  Oc Get  kind=Pod  namespace=test-pods
  Oc Delete  kind=Pod  name=my-pod  namespace=test-pods
  Oc Delete  kind=Pod  name=my-pod-1  namespace=test-pods
  Oc Delete  kind=Pod  name=my-pod-2  namespace=test-pods
  Oc Delete  kind=Project  name=test-pods

Test Generic Keywords Kind Event
  New Project  test-events
  Oc Get  kind=Event  namespace=redhat-ods-applications
  Oc Delete  kind=Project  name=test-events



