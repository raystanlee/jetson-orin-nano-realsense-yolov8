#!/bin/bash

sudo apt update

sudo apt install -y \
git \
libssl-dev \
libusb-1.0-0-dev \
pkg-config \
libgtk-3-dev \
libglfw3-dev \
libgl1-mesa-dev \
libglu1-mesa-dev \
cmake

git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
mkdir build
cd build

cmake .. -DBUILD_PYTHON_BINDINGS=true
make -j4
sudo make install