#!/bin/bash
set -e

ROOT_PATH=$(readlink ./setup.sh)
echo $ROOT_PATH
./setup.sh $ROOT_PATH