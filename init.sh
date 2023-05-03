#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*}
cd $DIR
set -ex

if ! [ -x "$(command -v direnv)" ]; then
  if ! [ -x "$(command -v apt-get)" ]; then
    apt-get install -y direnv
  fi
fi

direnv allow

pip install --upgrade pip
./sh/sharp.sh
pip install -r requirements.txt
if [ ! -d "$XXX" ]; then
  ./down.py
fi
