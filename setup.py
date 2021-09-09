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

from setuptools import setup, find_packages


DESCRIPTION = """
This test library provides  keywords to interact with
Openshift Cluster and perform various operations.
"""[1:-1]

setup(
    name='robotframework-OpenShiftCLI',
    version='1.0.0',
    description="Robotframework for OpenShift interactions via CLI",
    long_description=DESCRIPTION,
    author='Vasu Kulkarni',
    author_email='vasu@redhat.com',
    url='https://github.com/red-hat-data-services/robotframework-OpenShiftCLI',
    license='Apache License 2.0',
    keywords='robotframework openshift cli',
    platforms='any',
    install_requires=[
        "reportportal-client",
        "robotframework>=4",
        "robotframework-debuglibrary",
        "robotframework-seleniumlibrary",
        "robotframework-jupyterlibrary>=0.3.1",
        "ipython",
        "openshift",
        "pre-commit",
        "pytest",
        "pytest-logger",
        "pyyaml",
        "pygments",
        "requests",
        "Jinja2",
        "flake8",
        "mypy",
        "kubernetes",
        "validators"
    ],
    zip_safe=True,
    include_package_data=True,
    packages=find_packages(exclude=["tests"]),
)
