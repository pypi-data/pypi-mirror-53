#!/usr/bin/env bash
set -eu
./docker/build.sh
./docker/build.sh test
./docker/build.sh dev
# ./docker/build.sh docs
exit 0
