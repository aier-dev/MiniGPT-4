#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*}
cd $DIR
set -ex

direnv allow

pip install --upgrade pip
./sh/sharp.sh
pip install -r requirements.txt
if [ ! -d "$XXX" ]; then
  ./down.py
fi
