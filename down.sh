#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*}
cd $DIR
set -ex

if [ ! -d "model" ]; then
  pip install huggingface-hub
  ./down.py
fi
