# Robotframework Openshiftcli Library
Openshiftcli (a.k.a OpenshiftLibrary) is a robotframework library for [Kubernetes](https://kubernetes.io) and [OpenShift](https://openshift.com) APIs. The project is hosted on GitHub and downloads can be found from PyPI

# Installation
The recommended installation method is using pip:
```
pip install pip robotframework-openshiftcli
```
To install latest source from the master branch, use this command:
``` 
pip install git+https://github.com/red-hat-data-services/robotframework-openshiftcli.git
```
# Usage
## Keyword Documentation

To get the Documentation is necessary to be connected to a cluster with the oc command
```
python3 -m virtualenv .venv 
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 task.py
```
a new folder will be created /docs/ with the documentation openshiftcli.html

## Example

```
*** Settings ***
Documentation     openshiftcli Library
Library      openshiftcli

*** Test Cases ***
Test Generic Keywords Kind Project
   Oc New Project  test
   Oc Delete  kind=Project  name=test

```
