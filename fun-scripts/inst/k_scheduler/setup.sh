#!/bin/bash

# Parameter checking
if [ $# -lt 1 ]; then
  echo "<BUILD>: <KHOME>"
  exit 1
fi

# Prepare args
KHOME="$1"
pushd "$KHOME" || exit 1
export KHOME="$PWD"
popd || exit 1
# Create a dir to put afl-rt
OUT_DIR="$KHOME/afl-rt"

# set clang as llvm-11.0.1
export PATH="$KHOME"/libfuzzer_integration/llvm_11.0.1/build/bin:$PATH
# use wllvm as default compiler, make sure you are using llvm-11.0.1
export LLVM_COMPILER=clang
export CC=wllvm
export CXX=wllvm++
# Common compiler flags used in Google FuzzBench. Note that we add "-fsanitize-coverage=no-prune" to ensure a complete CFG intrumentation.
# @Adian: remove the usage of asan to avoid memory leak errors at building the project under test
export CFLAGS="-fsanitize-coverage=trace-pc-guard,no-prune -O2 -fno-omit-frame-pointer -gline-tables-only"
export CXXFLAGS="-fsanitize-coverage=trace-pc-guard,no-prune -O2 -fno-omit-frame-pointer -gline-tables-only"
# add the absolute path afl runtime library to LDFLAGS
export LDFLAGS="$OUT_DIR"/afl-llvm-rt.o

# Check envs
echo "PATH=$PATH"
echo "CC=$CC"
echo "CXX=$CXX"
echo "CFLAGS=$CFLAGS"
echo "CXXFLAGS=$CXXFLAGS"
echo "KHOME=$KHOME"
echo "ls -al $KHOME/afl-rt"
ls -al "$KHOME/afl-rt"
