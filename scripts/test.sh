#!/usr/bin/env bash

set -e

function cleanup {
    echo "Recent exit code: "$?
    rm -rf ./venv
}

trap cleanup EXIT

nosetests indor -v --with-coverage --cover-test --cover-package=indor --cover-min-percentage=75
python3 setup.py bdist_wheel --universal
virtualenv  ./venv
source ./venv/bin/activate
pip3 install dist/indor*
indor ./examples/sample_test.ind
rm -rf ./venv
