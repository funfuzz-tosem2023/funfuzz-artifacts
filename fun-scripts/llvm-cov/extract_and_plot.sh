#!/bin/bash

if [ ! $# -eq 1 ]; then
  echo "Usage <THIS_SCRIPT> <DATA_DIR>"
  exit 0
fi

DATA_DIR="$1"
pushd "$DATA_DIR" || exit 1
  DATA_DIR="$PWD"
popd || exit 1
RES_DIR="$DATA_DIR/_results"
DATA_CSV="$RES_DIR/data.csv"

SCRIPT_DIR=$(dirname "$0")
EXT_SCRIPT="$SCRIPT_DIR/extract_data_llvm_cov_region.py"
PLOT_SCRIPT="$SCRIPT_DIR/plot_cov_trend_region.py"

echo "python3 $EXT_SCRIPT $DATA_DIR"
python3 "$EXT_SCRIPT" "$DATA_DIR"

echo "python3 $PLOT_SCRIPT 0 $DATA_CSV $RES_DIR"
python3 "$PLOT_SCRIPT" 0 "$DATA_CSV" "$RES_DIR"
