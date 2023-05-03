#!/usr/bin/env bash

DIR=$(realpath $0) && DIR=${DIR%/*/*}
cd $DIR
set -ex

if [ -x "$(command -v apt-get)" ]; then
  apt-get update -y
  apt-get install -y ffmpeg libsm6 libxext6 \
    libpng-dev libjpeg-dev librsvg2-dev \
    libheif-dev libglib2.0-0 libglib2.0-dev \
    libwebp-dev meson libgirepository1.0-dev \
    libmagickcore-dev cmake make gcc g++
elif [ -x "$(command -v brew)" ]; then
  echo "Installing macOS packages..."
  brew install libpng jpeg librsvg libheif glib webp meson gobject-introspection imagemagick cmake make
else
  echo "Unsupported operating system."
  exit 1
fi

cd /tmp
if [ ! -d "libvips" ]; then
  # ver=$(curl -s https://api.github.com/repos/libvips/libvips/releases/latest | grep tag_name | cut -d '"' -f 4)
  # git clone -b $ver --depth=1 git@github.com:libvips/libvips.git
  git clone --depth=1 git@github.com:libvips/libvips.git
fi

cd libvips
meson build --libdir=lib --buildtype=release -Dintrospection=enabled # -Djpeg-xl=enabled
# --reconfigure
cd build
meson compile
meson test
meson install

cd $DIR
npm i sharp
rm -rf /tmp/libvips
