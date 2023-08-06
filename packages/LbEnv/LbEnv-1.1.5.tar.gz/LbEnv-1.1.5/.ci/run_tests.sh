#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Print each command before it is ran
set -x

if [ "$#" -ge 1 ] && [ "$1" == "PATCH_COVERAGE" ]; then
    # Patch the installation to include coverage for subprocesses
    # See: https://coverage.readthedocs.io/en/coverage-4.2/subprocess.html
    python -m pip install coverage
    cp always-include-coverage.pth "$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")"
    export COVERAGE_DATA_DIR=${PWD}
    export COVERAGE_PROCESS_START=$PWD/.coveragerc
fi

python --version
python -m pip install -e .
python setup.py nosetests --cover-package LbEnv
