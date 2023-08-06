#!/bin/sh -eu
PYTHONPATH=${PWD} pytest --cov=_sadm --cov-report=term --cov-report=html $@
exit 0
