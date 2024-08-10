#!/bin/bash

# Parameter checking
if [ $# -lt 2 ]; then
  echo "<BUILD>: <SUBJECT_DIR> <BENCH_DIR>"
  exit 1
fi

# Get abspath to subject directory
SUBJECT_DIR="$1"
pushd "$SUBJECT_DIR" || exit 1
  SUBJECT_DIR="$PWD"
popd || exit 1

# Get abspath to target directory
BENCH_DIR="$2"
pushd "$BENCH_DIR" || exit 1
  BENCH_DIR="$PWD"
popd || exit 1

# Choose compilers
export CC="$FUNFUZZ/afl-cc"
export CXX="$FUNFUZZ/afl-cc++"

# Some global settings
export AFL_FUN_TEMP="$SUBJECT_DIR/funtmp"
mkdir -p "$AFL_FUN_TEMP"
if [ -d "$AFL_FUN_TEMP" ]; then
  rm -rf "$AFL_FUN_TEMP"
fi
mkdir -p "$AFL_FUN_TEMP"
ASSIGN_ID_SCRIPT="$FUNFUZZ/fun/assign_func_id.py"
BUILD_CG_SCRIPT="$FUNFUZZ/fun/fs/construct_static_cg.py"

# Show configuration results
echo "==================== CONF-LOG ===================="
echo "SUBJECT_DIR=$SUBJECT_DIR"
echo "BENCH_DIR=$BENCH_DIR"
echo "CC=$CC"
echo "CXX=$CXX"
echo "AFL_FUN_TEMP=$AFL_FUN_TEMP"
echo "ASSIGN_ID_SCRIPT=$ASSIGN_ID_SCRIPT"
echo "BUILD_CG_SCRIPT=$BUILD_CG_SCRIPT"
echo "==================== CONF-LOG ===================="
sleep 3

# Two phase instrumentation
pushd "$SUBJECT_DIR" || exit 1

  # Clear outdated build
  ./autogen.sh
  ./configure --disable-shared
  make clean

  # --------------------------------------------- #
  # Phase1: Collect function info                 #
  # --------------------------------------------- #

  echo "==================== INST-LOG ===================="
  echo "(prefun) Collect function info..."
  echo "==================== INST-LOG ===================="
  sleep 3

  # May remove configuration history
  rm -f $(find . | grep "config.cache")

  # Emit prefun instrument
  export AFL_LLVM_INSTRUMENT="prefun"
  make xmllint

  # Remove prefun binaries
  make clean

  # Assign id for functions
  python3 "$ASSIGN_ID_SCRIPT" "$AFL_FUN_TEMP"

  # Build call graph, and compute static FS.
  python3 "$BUILD_CG_SCRIPT" "$AFL_FUN_TEMP"

  # --------------------------------------------- #
  # Phase2: Instrument direct calls for fun       #
  # --------------------------------------------- #

  echo "==================== INST-LOG ===================="
  echo "(fun) Perform fun-style instrumentation..."
  echo "==================== INST-LOG ===================="
  sleep 3

  # Emit fun instrument
  export AFL_LLVM_INSTRUMENT="fun"
  make xmllint

popd || exit 1

# Move target binary
TARGET="xmllint"
TARGET_DIR="$BENCH_DIR/$TARGET"
if [ -d "$TARGET_DIR" ]; then
  rm -rf "$TARGET_DIR"
fi
mkdir -p "$TARGET_DIR"
mv "$SUBJECT_DIR/$TARGET" "$TARGET_DIR" && cp -r "$AFL_FUN_TEMP" "$TARGET_DIR"
