#!/bin/bash
TEST_ARTIFACT_DIR="robotframework/output"

#TODO: Configure the "tmp_dir" creation so that we can have a "latest" link
TEST_ARTIFACT_DIR=$(mktemp -d -p ${TEST_ARTIFACT_DIR} -t ods-ci-$(date +%Y-%m-%d-%H-%M)-XXXXXXXXXX)

#run tests
robot -d ${TEST_ARTIFACT_DIR} -x xunit_test_result.xml -r test_report.html  robotframework/test.robot