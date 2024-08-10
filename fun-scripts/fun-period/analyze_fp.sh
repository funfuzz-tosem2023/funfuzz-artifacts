#!/bin/bash

set -x

if [ ! $# -eq 1 ]; then
  echo "Usage <THIS_SCRIPT> <DATA_DIR>"
  exit 0
fi

DATA_DIR="$1"
pushd "$DATA_DIR" || exit 1
  DATA_DIR="$PWD"
popd || exit 1

SCRIPT_DIR=$(dirname "$0")

FP_SCRIPT="$SCRIPT_DIR/r1_fun_period.py"
UTEST_SCRIPT="$SCRIPT_DIR/r1_fun_period_utest.py"

python3 $FP_SCRIPT $DATA_DIR
python3 $UTEST_SCRIPT $DATA_DIR
