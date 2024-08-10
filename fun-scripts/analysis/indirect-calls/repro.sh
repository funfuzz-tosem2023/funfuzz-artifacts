#/bin/bash

set +x

if [ $# -lt 1 ]; then
  echo "<repro-all>: <OUTS_DIR_NAME>"
  exit 0
fi


WORK_DIR="/indirect-calls"
PY_SCRIPT="$WORK_DIR/py/repro_by_target.py"
DYNAMORIO_HOME="$WORK_DIR/DynamoRIO-Linux-10.93.19908"
DYNAMORIO_CLIENT="$WORK_DIR/libinstrcalls.so"
FUZZ_OUTS="$WORK_DIR/$1"
TARGET_ROOT="$WORK_DIR/targets"
TUPPER=86400
TGAP=900
TIMEOUT=10

echo "FUZZ_OUTS=$FUZZ_OUTS"

# python3 py/repro_by_target.py ./aflpp-raw-outs/readpng/outs/ ./DynamoRIO-Linux-10.93.19908 ./libinstrcalls.so ./targets/readpng/readpng '' stdin 86400 900
python3 "$PY_SCRIPT" "$FUZZ_OUTS/cxxfilt/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/cxxfilt/cxxfilt" "" stdin $TUPPER $TGAP $TIMEOUT
python3 "$PY_SCRIPT" "$FUZZ_OUTS/nm-new/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/nm-new/nm-new" "" file $TUPPER $TGAP $TIMEOUT
python3 "$PY_SCRIPT" "$FUZZ_OUTS/objdump/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/objdump/objdump" "-d" file $TUPPER $TGAP $TIMEOUT
python3 "$PY_SCRIPT" "$FUZZ_OUTS/readelf/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/readelf/readelf" "-a" file $TUPPER $TGAP $TIMEOUT
python3 "$PY_SCRIPT" "$FUZZ_OUTS/djpeg/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/djpeg/djpeg" "" file $TUPPER $TGAP $TIMEOUT
python3 "$PY_SCRIPT" "$FUZZ_OUTS/readpng/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/readpng/readpng" "" stdin $TUPPER $TGAP $TIMEOUT
python3 "$PY_SCRIPT" "$FUZZ_OUTS/mjs/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/mjs/mjs" "-f" file $TUPPER $TGAP $TIMEOUT
python3 "$PY_SCRIPT" "$FUZZ_OUTS/mutool/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/mutool/mutool" "draw" file $TUPPER $TGAP $TIMEOUT
python3 "$PY_SCRIPT" "$FUZZ_OUTS/tcpdump/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/tcpdump/tcpdump" "" file $TUPPER $TGAP $TIMEOUT
python3 "$PY_SCRIPT" "$FUZZ_OUTS/xmllint/outs/" "$DYNAMORIO_HOME" "$DYNAMORIO_CLIENT" "$TARGET_ROOT/xmllint/xmllint" "" file $TUPPER $TGAP $TIMEOUT
