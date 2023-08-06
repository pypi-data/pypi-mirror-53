#!/usr/bin/env bash
set -eu
TAG=${1:-''}
IMAGE='jrmsdev/sadm'
NAME='sadm'
if test "X${TAG}" != 'X'; then
	shift
	IMAGE="jrmsdev/sadm:${TAG}"
	NAME="sadm${TAG}"
fi
ENVVARS=''
if test "${TAG}" = 'dev' || test "${TAG}" = 'docs'; then
	ENVVARS='-e PYTHONPATH=/opt/src/sadm'
fi
if test "${TAG}" = 'dev' || test "${TAG}" = 'test'; then
	ENVVARS="${ENVVARS} -e SADMTEST_LOG=debug"
fi
docker run -it --rm --name=${NAME} --hostname=${NAME} --user sadm \
	-p 3666:80 -v ${PWD}:/opt/src/sadm ${ENVVARS} ${IMAGE} $@
exit 0
