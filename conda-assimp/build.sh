#!/bin/bash
mkdir build
cd build

CMAKE_GENERATOR="Unix Makefiles"
CMAKE_ARCH="-m"$ARCH

if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  export CFLAGS="$CFLAGS $CMAKE_ARCH"
  export LDLAGS="$LDLAGS $CMAKE_ARCH"
fi

cmake .. -G"$CMAKE_GENERATOR" \
-DENABLE_BOOST_WORKAROUND=1 \
-DBUILD_ASSIMP_TOOLS=0 \
-DCMAKE_INSTALL_PREFIX=$PREFIX

make
make install

