#!/bin/bash

#############################################
# Based on K-scheduler official scripts.
# Use source to make global environments.
#############################################

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
if [ -e "$OUT_DIR" ]; then
  rm -rf "$OUT_DIR"
  echo "Create $OUT_DIR"...
fi
mkdir "$OUT_DIR"

echo "KHOME=$KHOME"
echo "OUT_DIR=$OUT_DIR"

# Require wllvm (may install)
pip3 install wllvm

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

# Go into out dir
pushd "$OUT_DIR" || exit 1

# build afl runtime library
$CC -O2 -c -w "$KHOME"/afl_integration/afl-2.52b_kscheduler/llvm_mode/afl-llvm-rt.o.c -o afl-llvm-rt.o
# build afl driver
$CXX -std=c++11 -O2 -c "$KHOME"/libfuzzer_integration/llvm_11.0.1/compiler-rt/lib/fuzzer/afl/afl_driver.cpp
ar r afl_llvm_rt_driver.a afl_driver.o afl-llvm-rt.o

popd || exit 1

# add the absolute path afl runtime library to LDFLAGS
export LDFLAGS="$OUT_DIR"/afl-llvm-rt.o

# Check envs
echo "PATH=$PATH"
echo "CC=$CC"
echo "CXX=$CXX"
echo "CFLAGS=$CFLAGS"
echo "CXXFLAGS=$CXXFLAGS"
echo "KHOME=$KHOME"
echo "ls -al $OUT_DIR"
ls -al "$OUT_DIR"
