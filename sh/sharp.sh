#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*/*}
cd $DIR
set -ex

LIB=$(python -c "import sysconfig;print(sysconfig.get_config_var('LIBPL'))")
export LIBRARY_PATH=$LIB:$LIBRARY_PATH

if [ -x "$(command -v apt-get)" ]; then
  apt-get update -y
  apt-get install ffmpeg libsm6 libxext6 -y
fi

if [ "$os_type" == "Darwin" ]; then
  # macOS
  echo "Installing macOS packages..."
  brew install libpng jpeg librsvg libheif glib webp meson gobject-introspection imagemagick cmake make
elif [ "$os_type" == "Linux" ]; then
  # Linux
  echo "Installing Linux packages..."
  apt-get install -y libpng-dev libjpeg-dev librsvg2-dev \
    libheif-dev libglib2.0-0 libglib2.0-dev \
    libwebp-dev meson libgirepository1.0-dev libmagickcore-dev cmake make gcc g++
else
  echo "Unsupported operating system."
  exit 1
fi

cd /tmp
if [ ! -d "libvips" ]; then
  git clone --depth=1 git@github.com:libvips/libvips.git
fi

wait
cd libvips
meson build --libdir=lib --buildtype=release -Dintrospection=enabled -Djpeg-xl=enabled
# --reconfigure
cd build
meson compile
meson test
meson install

cd $DIR
npm i @w5/py sharp
rm -rf /tmp/libvips
