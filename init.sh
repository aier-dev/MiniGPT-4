#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*}
cd $DIR
set -ex

pip install --upgrade pip
./sh/sharp.sh
pip install -r requirements.txt
./down.sh
