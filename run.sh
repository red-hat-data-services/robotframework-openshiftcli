#!/bin/bash
TEST_ARTIFACT_DIR="robotframework/output"
TEST_CASE_FILE=robotframework/test-generic
TEST_VARIABLES=""


while [ "$#" -gt 0 ]; do
  case $1 in
    # Override/Add global variables specified in the test variables file
    --test-variable)
      shift
      TEST_VARIABLES="${TEST_VARIABLES} --variable $1"
      shift
      ;;

    # Specify test case to run
    --test-case)
      shift
      TEST_CASE_FILE=$1
      shift
      ;;

    *)
      echo "Unknown command line switch: $1"
      exit 1
      ;;
  esac
done

#TODO: Configure the "tmp_dir" creation so that we can have a "latest" link
TEST_ARTIFACT_DIR=$(mktemp -d -p ${TEST_ARTIFACT_DIR} -t ods-ci-$(date +%Y-%m-%d-%H-%M)-XXXXXXXXXX)

#run tests
robot --pythonpath . -d ${TEST_ARTIFACT_DIR} -x xunit_test_result.xml -r test_report.html ${TEST_VARIABLES} ${TEST_CASE_FILE}
