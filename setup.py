#!/usr/bin/env python

#  Copyright 2013-2014 NaviNet Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
from os.path import join, dirname
from setuptools import setup, find_packages

sys.path.append(join(dirname(__file__), 'OpenShiftCLI'))

DESCRIPTION = """
This test library provides  keywords to interact with
Openshift Cluster and perform various operations.
"""[1:-1]

setup(
    name='robotframework-OpenShiftCLI',
    version='v0.1',
    description="Robotframework for OpenShift interactions via CLI",
    long_description=DESCRIPTION,
    author='Vasu Kulkarni',
    author_email='vasu@redhat.com',
    url='https://github.com/vasukulkarni/robotframework-OpenShiftCLI',
    license='Apache License 2.0',
    keywords='robotframework openshift cli',
    platforms='any',
    install_requires=[
        'robotframework',
    ],
    packages=['OpenShiftCLI'],
)
