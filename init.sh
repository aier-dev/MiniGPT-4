#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*}
cd $DIR
set -ex

pip install --upgrade pip
pip install -r requirements.txt

if [[ $(uname) != *"Darwin"* ]]; then
  pip install decord
else
  pip3 install --upgrade --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/cpu
  pip install eva-decord
fi
#./sh/sharp.sh
./down.sh
