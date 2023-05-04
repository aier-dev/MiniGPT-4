#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*}
cd $DIR
set -ex

pip install --upgrade pip
pip install -r requirements.txt

if [[ $(uname) != *"Darwin"* ]]; then
  pip install eva-decord
else
  pip install decord
fi
#./sh/sharp.sh
./down.sh
