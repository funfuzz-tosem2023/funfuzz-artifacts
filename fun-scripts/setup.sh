# Setup experimental environments
WORKING_DIR="/root/qrx/aflpp_fun"
export AFLPP="$WORKING_DIR/AFLplusplus-4.04c"   # make source-only
export FUNFUZZ="$WORKING_DIR/aflpp-fun"         # make source-only
export FAIRFUZZ="$WORKING_DIR/fairfuzz"         # git checkout aflpp-plot; make; cd llvm_mode; make; cd -
export SCRIPTS="$WORKING_DIR/fun-scripts"
export SEEDS="$FUNFUZZ/testcases"

# Check settings
echo "AFLPP=$AFLPP"
echo "FUNFUZZ=$FUNFUZZ"
echo "FAIRFUZZ=$FAIRFUZZ"
echo "SCRIPTS=$SCRIPTS"
echo "SEEDS=$SEEDS"

# Modify system dump
echo "Modify system dump: echo core > /proc/sys/kernel/core_pattern"
echo "core" > /proc/sys/kernel/core_pattern
