#!/bin/sh
MAKE_ARCH="-m"$ARCH

if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  export CFLAGS="$CFLAGS $MAKE_ARCH"
  export LDLAGS="$LDLAGS $MAKE_ARCH"
fi

CFLAGS="-I$PREFIX/include $CFLAGS" LDFLAGS="-L$PREFIX/lib $LDFLAGS" "$PYTHON" setup.py install
