#!/usr/bin/env bash
set -eu
TAG=${1:-''}
IMAGE='jrmsdev/sadm'
DOCKERFN='Dockerfile'
if test "X${TAG}" != "X"; then
	IMAGE="jrmsdev/sadm:${TAG}"
	DOCKERFN="Dockerfile.${TAG}"
fi
docker build \
	--build-arg SADM_UID=$(id -u) \
	--build-arg SADM_GID=$(id -g) \
	-t ${IMAGE} -f docker/${DOCKERFN} .
exit 0
