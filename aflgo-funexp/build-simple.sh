##############################
### Build AFLGo components ###
##############################

export CXX=`which clang++`
export CC=`which clang`
export LLVM_CONFIG=`which llvm-config`

pushd afl-2.57b
make clean all
popd

pushd instrument
make clean all
popd

pushd distance/distance_calculator
cmake ./
cmake --build ./
popd

echo -e '\x1b[0;36mAFLGo (yeah!) \x1b[0;32mbuild is done \x1b[0m'
#########   cCYA   #############    cGRN   ############# cRST ###
