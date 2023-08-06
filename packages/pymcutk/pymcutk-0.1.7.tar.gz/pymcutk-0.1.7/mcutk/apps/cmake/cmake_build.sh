#!/bin/sh
cd $1
rm -rf CMakeFiles $2
rm -rf Makefile cmake_install.cmake CMakeCache.txt
cmake -DCMAKE_TOOLCHAIN_FILE=$3 -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=$2
if [ $? != 0 ];then
exit $?
fi
make -C . -j4
exit $?
