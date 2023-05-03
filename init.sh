#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*}
cd $DIR
set -ex

if ! [ -x "$(command -v rtx)" ]; then
  curl https://rtx.pub/install.sh | sh
  echo -e "\neval \"\$($HOME/.local/share/rtx/bin/rtx activate -s bash)\"" >>~/.bashrc
  eval $($HOME/.local/share/rtx/bin/rtx env)
  source ~/.bashrc
fi

rtx install

if ! [ -x "$(command -v direnv)" ]; then
  if ! [ -x "$(command -v apt-get)" ]; then
    apt-get install -y direnv
    echo -e "eval \"\$(direnv hook bash)\"" >>~/.bashrc
    source ~/.bashrc
  fi
fi

direnv allow

pip install --upgrade pip
./sh/sharp.sh
pip install -r requirements.txt

if [ ! -d "model" ]; then
  ./down.py
fi
