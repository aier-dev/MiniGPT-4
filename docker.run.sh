#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*}
cd $DIR
set -ex

docker run -v ./model:/app/model --rm -it minigpt4 /bin/bash
