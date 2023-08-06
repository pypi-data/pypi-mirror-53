#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Print each command before it is ran
set -x

python --version
python setup.py nosetests --cover-package LbPlatformUtils
mkdir -p cover_report && mv -f cover "cover_report/${CI_JOB_NAME}"
python setup.py install && lb-describe-platform --flags
