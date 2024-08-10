## Commands to run aflgo with all the functions specified as targets.

The assumed structure of the working directory:

```
.
├── aflgo
│   └── (aflgo stuffs) ...
├── data
|   ├── xmllint
│   └── (one target for each) ...
└── subjects
    ├── libxml2-2.9.4
    └── (one project for each) ...
```

### Libxml-2.9.4 - {xmllint} 

#### 0 Build

The build is basically follows [aflgo's README](https://github.com/aflgo/aflgo?tab=readme-ov-file) (How to instrument with AFLGo step 6~8).

```shell
# Prepare env
cd <work_dir>
export AFLGO=$PWD/aflgo
export SUBJECT=$PWD/subjects/libxml2-2.9.4
export TMP_DIR=$SUBJECT/temp
mkdir $TMP_DIR
# Compile pass and compiler for extracting functions. 
cd $AFLGO/instrument && make && cd -
# Dump all functions.
export CC=$AFLGO/instrument/fundump-clang
export CXX=$AFLGO/instrument/fundump-clang++
export CFLAGS="-outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CXXFLAGS="$CFLAGS"
export LDFLAGS=-lpthread
pushd $SUBJECT
  ./autogen.sh
  ./configure --disable-shared
  make clean
  make -j8 xmllint
popd
# Check whether Fdumps.txt file is correctly generated.
cat $TMP_DIR/Fdumps.txt
# Turn Fdumps.txt into BBtargets.txt file.
python3 $AFLGO/instrument/fundump2BBtargets.py $TMP_DIR
# Check whether BBtargets.txt file is correctly generated.
cat $TMP_DIR/BBtargets.txt

# Then come into aflgo instrument process.
unset CC CXX CFLAGS CXXFLAGS
# Set aflgo-instrumenter
export CC=$AFLGO/instrument/aflgo-clang
export CXX=$AFLGO/instrument/aflgo-clang++
# Set aflgo-instrumentation flags
export COPY_CFLAGS=$CFLAGS
export COPY_CXXFLAGS=$CXXFLAGS
export ADDITIONAL="-targets=$TMP_DIR/BBtargets.txt -outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CFLAGS="$CFLAGS $ADDITIONAL"
export CXXFLAGS="$CXXFLAGS $ADDITIONAL"
# Build libxml2 (in order to generate CG and CFGs).
# Meanwhile go have a coffee ☕️
export LDFLAGS=-lpthread
pushd $SUBJECT
  ./autogen.sh
  ./configure --disable-shared
  make clean
  make xmllint
popd
# Clean up to avoid distance calculation to fail.
cat $TMP_DIR/BBnames.txt | grep -v "^$"| rev | cut -d: -f2- | rev | sort | uniq > $TMP_DIR/BBnames2.txt && mv $TMP_DIR/BBnames2.txt $TMP_DIR/BBnames.txt
cat $TMP_DIR/BBcalls.txt | grep -Ev "^[^,]*$|^([^,]*,){2,}[^,]*$"| sort | uniq > $TMP_DIR/BBcalls2.txt && mv $TMP_DIR/BBcalls2.txt $TMP_DIR/BBcalls.txt
# Generate distance ☕️
# $AFLGO/distance/gen_distance_orig.sh is the original, but significantly slower, version
$AFLGO/distance/gen_distance_fast.py $SUBJECT $TMP_DIR xmllint
# Instrument the distances
export CFLAGS="$COPY_CFLAGS -distance=$TMP_DIR/distance.cfg.txt"
export CXXFLAGS="$COPY_CXXFLAGS -distance=$TMP_DIR/distance.cfg.txt"
# Clean and build subject with distance instrumentation ☕️
pushd $SUBJECT
  make clean
  ./configure --disable-shared
  make -j8 xmllint
popd
```

#### 1 Run

```shell
export TARGET=xmllint
export AFLGO=$PWD/aflgo
export DATA_DIR=$PWD/data
export SUBJECT=$PWD/subjects/libxml2-2.9.4
mkdir -p $DATA_DIR/$TARGET/outs
timeout 86405s $AFLGO/afl-2.57b/afl-fuzz -z exp -c 45m -i $SUBJECT/in -o $DATA_DIR/$TARGET/outs/out- $SUBJECT/$TARGET @@
```

### Binutils-2.28 - {cxxfilt, readelf, objdump, nm-new}

#### 0 Build

```shell
cd <work_dir>
export AFLGO=$PWD/aflgo
export SUBJECT=$PWD/subjects/binutils-2.28
export TMP_DIR=$SUBJECT/temp
mkdir $TMP_DIR
# Compile pass and compiler for extracting functions. 
cd $AFLGO/instrument && make && cd -
# Dump all functions.
export CC=$AFLGO/instrument/fundump-clang
export CXX=$AFLGO/instrument/fundump-clang++
export CFLAGS="-outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CXXFLAGS="$CFLAGS"
export LDFLAGS=-lpthread
pushd $SUBJECT
  rm -f $(find . | grep "config.cache")
  ./configure --disable-shared
  make clean
  make
popd
# Check whether Fdumps.txt file is correctly generated.
cat $TMP_DIR/Fdumps.txt
# Turn Fdumps.txt into BBtargets.txt file.
python3 $AFLGO/instrument/fundump2BBtargets.py $TMP_DIR
# Check whether BBtargets.txt file is correctly generated.
cat $TMP_DIR/BBtargets.txt

# Then come into aflgo instrument process.
unset CC CXX CFLAGS CXXFLAGS
# Set aflgo-instrumenter
export CC=$AFLGO/instrument/aflgo-clang
export CXX=$AFLGO/instrument/aflgo-clang++
# Set aflgo-instrumentation flags
export COPY_CFLAGS=$CFLAGS
export COPY_CXXFLAGS=$CXXFLAGS
export ADDITIONAL="-targets=$TMP_DIR/BBtargets.txt -outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CFLAGS="$CFLAGS $ADDITIONAL"
export CXXFLAGS="$CXXFLAGS $ADDITIONAL"
export LDFLAGS=-lpthread
pushd $SUBJECT
  rm -f $(find . | grep "config.cache")
  ./configure --disable-shared
  make clean
  make
popd
# Clean up to avoid distance calculation to fail.
cat $TMP_DIR/BBnames.txt | grep -v "^$"| rev | cut -d: -f2- | rev | sort | uniq > $TMP_DIR/BBnames2.txt && mv $TMP_DIR/BBnames2.txt $TMP_DIR/BBnames.txt
cat $TMP_DIR/BBcalls.txt | grep -Ev "^[^,]*$|^([^,]*,){2,}[^,]*$"| sort | uniq > $TMP_DIR/BBcalls2.txt && mv $TMP_DIR/BBcalls2.txt $TMP_DIR/BBcalls.txt
# Generate distance ☕️
# $AFLGO/distance/gen_distance_orig.sh is the original, but significantly slower, version
export TARGET=[readelf|cxxfilt|objdump|nm-new]
$AFLGO/distance/gen_distance_fast.py $SUBJECT/binutils $TMP_DIR $TARGET
# Rename the distance file concerning different targets.
mv $TMP_DIR/distance.cfg.txt $TMP_DIR/distance.cfg.txt.$TARGET
# Build for each of the target and mv them out 
mkdir $SUBJECT/dist-targets
# Instrument the distances
export CFLAGS="$COPY_CFLAGS -distance=$TMP_DIR/distance.cfg.txt.$TARGET"
export CXXFLAGS="$COPY_CXXFLAGS -distance=$TMP_DIR/distance.cfg.txt.$TARGET"
# Clean and build subject with distance instrumentation ☕️
pushd $SUBJECT
  rm -f $(find . | grep "config.cache")
  ./configure --disable-shared
  make clean
  make -j8
popd
# Check binary
ll -h $SUBJECT/binutils/$TARGET
mv $SUBJECT/binutils/$TARGET $SUBJECT/dist-targets
```

#### 1 Run

cxxfilt
```shell
export TARGET=cxxfilt 
export AFLGO=$PWD/aflgo
export DATA_DIR=$PWD/data
export IN_DIR=$DATA_DIR/$TARGET/in
export SUBJECT=$PWD/subjects/binutils-2.28
mkdir -p $DATA_DIR/$TARGET/outs
# Prepare seed
mkdir -p $IN_DIR
echo "_Z1fv" > $IN_DIR/seed
timeout 86405s $AFLGO/afl-2.57b/afl-fuzz -z exp -c 45m -i $IN_DIR -o $DATA_DIR/$TARGET/outs/out- $SUBJECT/dist-targets/$TARGET
```

nm-new
```shell
export AFLPP=<path-to-aflpp>
export TARGET=nm-new 
export AFLGO=$PWD/aflgo
export DATA_DIR=$PWD/data
export IN_DIR=$DATA_DIR/$TARGET/in
export SUBJECT=$PWD/subjects/binutils-2.28
mkdir -p $DATA_DIR/$TARGET/outs
# Prepare seed
mkdir -p $IN_DIR
cp $AFLPP/testcases/others/elf/*.elf "$IN_DIR"
timeout 86405s $AFLGO/afl-2.57b/afl-fuzz -z exp -c 45m -i $IN_DIR -o $DATA_DIR/$TARGET/outs/out- $SUBJECT/dist-targets/$TARGET @@
```

readelf
```shell
export AFLPP=<path-to-aflpp>
export TARGET=readelf 
export AFLGO=$PWD/aflgo
export DATA_DIR=$PWD/data
export IN_DIR=$DATA_DIR/$TARGET/in
export SUBJECT=$PWD/subjects/binutils-2.28
mkdir -p $DATA_DIR/$TARGET/outs
# Prepare seed
mkdir -p $IN_DIR
cp $AFLPP/testcases/others/elf/*.elf "$IN_DIR"
timeout 86405s $AFLGO/afl-2.57b/afl-fuzz -z exp -c 45m -i $IN_DIR -o $DATA_DIR/$TARGET/outs/out- $SUBJECT/dist-targets/$TARGET -a @@
```

objdump
```shell
export AFLPP=<path-to-aflpp>
export TARGET=objdump 
export AFLGO=$PWD/aflgo
export DATA_DIR=$PWD/data
export IN_DIR=$DATA_DIR/$TARGET/in
export SUBJECT=$PWD/subjects/binutils-2.28
mkdir -p $DATA_DIR/$TARGET/outs
# Prepare seed
mkdir -p $IN_DIR
cp $AFLPP/testcases/others/elf/*.elf "$IN_DIR"
timeout 86405s $AFLGO/afl-2.57b/afl-fuzz -z exp -c 45m -i $IN_DIR -o $DATA_DIR/$TARGET/outs/out- $SUBJECT/dist-targets/$TARGET -d @@
```

### Mjs-2.20.0

#### 0 Build

```shell
# Prepare env
cd <work_dir>
export AFLGO=$PWD/aflgo
export SUBJECT=$PWD/subjects/mjs-2.20.0
export TMP_DIR=$SUBJECT/temp
mkdir $TMP_DIR
# Compile pass and compiler for extracting functions. 
cd $AFLGO/instrument && make && cd -
# Dump all functions.
export CC=$AFLGO/instrument/fundump-clang
export CXX=$AFLGO/instrument/fundump-clang++
export CFLAGS="-outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CXXFLAGS="$CFLAGS"
export LDFLAGS=-lpthread
pushd $SUBJECT
  rm mjs
  $CC $CFLAGS -DMJS_MAIN mjs.c -ldl -g -o mjs
popd
# Check whether Fdumps.txt file is correctly generated.
cat $TMP_DIR/Fdumps.txt
# Turn Fdumps.txt into BBtargets.txt file.
python3 $AFLGO/instrument/fundump2BBtargets.py $TMP_DIR
# Check whether BBtargets.txt file is correctly generated.
cat $TMP_DIR/BBtargets.txt

# Then come into aflgo instrument process.
unset CC CXX CFLAGS CXXFLAGS
# Set aflgo-instrumenter
export CC=$AFLGO/instrument/aflgo-clang
export CXX=$AFLGO/instrument/aflgo-clang++
# Set aflgo-instrumentation flags
export COPY_CFLAGS=$CFLAGS
export COPY_CXXFLAGS=$CXXFLAGS
export ADDITIONAL="-targets=$TMP_DIR/BBtargets.txt -outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CFLAGS="$CFLAGS $ADDITIONAL"
export CXXFLAGS="$CXXFLAGS $ADDITIONAL"
# Build libxml2 (in order to generate CG and CFGs).
# Meanwhile go have a coffee ☕️
export LDFLAGS=-lpthread
pushd $SUBJECT
  rm mjs
  $CC $CFLAGS -DMJS_MAIN mjs.c -ldl -g -o mjs
popd
# Clean up to avoid distance calculation to fail.
cat $TMP_DIR/BBnames.txt | grep -v "^$"| rev | cut -d: -f2- | rev | sort | uniq > $TMP_DIR/BBnames2.txt && mv $TMP_DIR/BBnames2.txt $TMP_DIR/BBnames.txt
cat $TMP_DIR/BBcalls.txt | grep -Ev "^[^,]*$|^([^,]*,){2,}[^,]*$"| sort | uniq > $TMP_DIR/BBcalls2.txt && mv $TMP_DIR/BBcalls2.txt $TMP_DIR/BBcalls.txt
# Generate distance ☕️
# $AFLGO/distance/gen_distance_orig.sh is the original, but significantly slower, version
$AFLGO/distance/gen_distance_fast.py $SUBJECT $TMP_DIR mjs
# Instrument the distances
export CFLAGS="$COPY_CFLAGS -distance=$TMP_DIR/distance.cfg.txt"
export CXXFLAGS="$COPY_CXXFLAGS -distance=$TMP_DIR/distance.cfg.txt"
# Clean and build subject with distance instrumentation ☕️
pushd $SUBJECT
  rm mjs
  $CC $CFLAGS -DMJS_MAIN mjs.c -ldl -g -o mjs
popd
```

#### 1 Run

```shell
export AFLPP=<path-to-aflpp>
export TARGET=mjs 
export AFLGO=$PWD/aflgo
export DATA_DIR=$PWD/data
export IN_DIR=$DATA_DIR/$TARGET/in
export SUBJECT=$PWD/subjects/mjs-2.20.0
mkdir -p $DATA_DIR/$TARGET/outs
# Prepare seed
mkdir -p $IN_DIR
cp $AFLPP/testcases/others/js/*.js "$IN_DIR"
timeout 86405s $AFLGO/afl-2.57b/afl-fuzz -z exp -c 45m -i $IN_DIR -o $DATA_DIR/$TARGET/outs/out- $SUBJECT/$TARGET -f @@
```

### Libjpeg-jpeg-turbo-1.5.1

#### 0 Build

```shell
# Prepare env
cd <work_dir>
export AFLGO=$PWD/aflgo
export SUBJECT=$PWD/subjects/libjpeg-turbo-1.5.1
export TMP_DIR=$SUBJECT/temp
mkdir $TMP_DIR
# Compile pass and compiler for extracting functions. 
cd $AFLGO/instrument && make && cd -
# Dump all functions.
export CC=$AFLGO/instrument/fundump-clang
export CXX=$AFLGO/instrument/fundump-clang++
export CFLAGS="-outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CXXFLAGS="$CFLAGS"
export LDFLAGS=-lpthread
pushd $SUBJECT
  autoreconf -fiv
  ./configure --disable-shared
  make clean
  make
popd
# Check whether Fdumps.txt file is correctly generated.
cat $TMP_DIR/Fdumps.txt
# Turn Fdumps.txt into BBtargets.txt file.
python3 $AFLGO/instrument/fundump2BBtargets.py $TMP_DIR
# Check whether BBtargets.txt file is correctly generated.
cat $TMP_DIR/BBtargets.txt

# Then come into aflgo instrument process.
unset CC CXX CFLAGS CXXFLAGS
# Set aflgo-instrumenter
export CC=$AFLGO/instrument/aflgo-clang
export CXX=$AFLGO/instrument/aflgo-clang++
# Set aflgo-instrumentation flags
export COPY_CFLAGS=$CFLAGS
export COPY_CXXFLAGS=$CXXFLAGS
export ADDITIONAL="-targets=$TMP_DIR/BBtargets.txt -outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CFLAGS="$CFLAGS $ADDITIONAL"
export CXXFLAGS="$CXXFLAGS $ADDITIONAL"
# Build libxml2 (in order to generate CG and CFGs).
# Meanwhile go have a coffee ☕️
export LDFLAGS=-lpthread
pushd $SUBJECT
  autoreconf -fiv
  ./configure --disable-shared
  make clean
  make
popd
# Clean up to avoid distance calculation to fail.
cat $TMP_DIR/BBnames.txt | grep -v "^$"| rev | cut -d: -f2- | rev | sort | uniq > $TMP_DIR/BBnames2.txt && mv $TMP_DIR/BBnames2.txt $TMP_DIR/BBnames.txt
cat $TMP_DIR/BBcalls.txt | grep -Ev "^[^,]*$|^([^,]*,){2,}[^,]*$"| sort | uniq > $TMP_DIR/BBcalls2.txt && mv $TMP_DIR/BBcalls2.txt $TMP_DIR/BBcalls.txt
# Generate distance ☕️
# $AFLGO/distance/gen_distance_orig.sh is the original, but significantly slower, version
$AFLGO/distance/gen_distance_fast.py $SUBJECT $TMP_DIR djpeg
# Instrument the distances
export CFLAGS="$COPY_CFLAGS -distance=$TMP_DIR/distance.cfg.txt"
export CXXFLAGS="$COPY_CXXFLAGS -distance=$TMP_DIR/distance.cfg.txt"
# Clean and build subject with distance instrumentation ☕️
pushd $SUBJECT
  autoreconf -fiv
  ./configure --disable-shared
  make clean
  make
popd
```

#### 1 Run

```shell
export AFLPP=<path-to-aflpp>
export TARGET=djpeg 
export AFLGO=$PWD/aflgo
export DATA_DIR=$PWD/data
export IN_DIR=$DATA_DIR/$TARGET/in
export SUBJECT=$PWD/subjects/libjpeg-turbo-1.5.1
mkdir -p $DATA_DIR/$TARGET/outs
# Prepare seed
mkdir -p $IN_DIR
cp $AFLPP/testcases/images/jpeg/*.jpg "$IN_DIR"
timeout 86405s $AFLGO/afl-2.57b/afl-fuzz -z exp -c 45m -i $IN_DIR -o $DATA_DIR/$TARGET/outs/out- $SUBJECT/$TARGET @@
```

### Libpng-1.6.29

#### 0 Build

```shell
# Prepare env
cd <work_dir>
export AFLGO=$PWD/aflgo
export SUBJECT=$PWD/subjects/libpng-1.6.29
export TMP_DIR=$SUBJECT/temp
mkdir $TMP_DIR
# Compile pass and compiler for extracting functions. 
cd $AFLGO/instrument && make && cd -
# Dump all functions.
export CC=$AFLGO/instrument/fundump-clang
export CXX=$AFLGO/instrument/fundump-clang++
export CFLAGS="-outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CXXFLAGS="$CFLAGS"
export LDFLAGS=-lpthread
pushd $SUBJECT
  # Build libs
  ./configure --disable-shared
  make clean
  make
  # Build readpng
  $CC $CFLAGS -o readpng ./contrib/libtests/readpng.c ./.libs/libpng16.a -lz -lm
popd
# Check whether Fdumps.txt file is correctly generated.
cat $TMP_DIR/Fdumps.txt
# Turn Fdumps.txt into BBtargets.txt file.
python3 $AFLGO/instrument/fundump2BBtargets.py $TMP_DIR
# Check whether BBtargets.txt file is correctly generated.
cat $TMP_DIR/BBtargets.txt

# Then come into aflgo instrument process.
unset CC CXX CFLAGS CXXFLAGS
# Set aflgo-instrumenter
export CC=$AFLGO/instrument/aflgo-clang
export CXX=$AFLGO/instrument/aflgo-clang++
# Set aflgo-instrumentation flags
export COPY_CFLAGS=$CFLAGS
export COPY_CXXFLAGS=$CXXFLAGS
export ADDITIONAL="-targets=$TMP_DIR/BBtargets.txt -outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CFLAGS="$CFLAGS $ADDITIONAL"
export CXXFLAGS="$CXXFLAGS $ADDITIONAL"
# Build libxml2 (in order to generate CG and CFGs).
# Meanwhile go have a coffee ☕️
export LDFLAGS=-lpthread
pushd $SUBJECT
  # Build libs
  ./configure --disable-shared
  make clean
  make
  # Build readpng
  $CC $CFLAGS -o readpng ./contrib/libtests/readpng.c ./.libs/libpng16.a -lz -lm
popd
# Clean up to avoid distance calculation to fail.
cat $TMP_DIR/BBnames.txt | grep -v "^$"| rev | cut -d: -f2- | rev | sort | uniq > $TMP_DIR/BBnames2.txt && mv $TMP_DIR/BBnames2.txt $TMP_DIR/BBnames.txt
cat $TMP_DIR/BBcalls.txt | grep -Ev "^[^,]*$|^([^,]*,){2,}[^,]*$"| sort | uniq > $TMP_DIR/BBcalls2.txt && mv $TMP_DIR/BBcalls2.txt $TMP_DIR/BBcalls.txt
# Generate distance ☕️
# $AFLGO/distance/gen_distance_orig.sh is the original, but significantly slower, version
$AFLGO/distance/gen_distance_fast.py $SUBJECT $TMP_DIR readpng
# Instrument the distances
export CFLAGS="$COPY_CFLAGS -distance=$TMP_DIR/distance.cfg.txt"
export CXXFLAGS="$COPY_CXXFLAGS -distance=$TMP_DIR/distance.cfg.txt"
# Clean and build subject with distance instrumentation ☕️
pushd $SUBJECT
  # Build libs
  ./configure --disable-shared
  make clean
  make
  # Build readpng
  $CC $CFLAGS -o readpng ./contrib/libtests/readpng.c ./.libs/libpng16.a -lz -lm
popd
```

#### 1 Run

```shell
export AFLPP=<path-to-aflpp>
export TARGET=readpng 
export AFLGO=$PWD/aflgo
export DATA_DIR=$PWD/data
export IN_DIR=$DATA_DIR/$TARGET/in
export SUBJECT=$PWD/subjects/libpng-1.6.29
mkdir -p $DATA_DIR/$TARGET/outs
# Prepare seed
mkdir -p $IN_DIR
cp $AFLPP/testcases/images/png/not_kitty.png  "$IN_DIR"
timeout 86405s $AFLGO/afl-2.57b/afl-fuzz -z exp -c 45m -i $IN_DIR -o $DATA_DIR/$TARGET/outs/out- $SUBJECT/$TARGET
```

### Tcpdump-4.9.0

#### 0 Build

```shell
# Prepare env
cd <work_dir>
export AFLGO=$PWD/aflgo
export SUBJECT=$PWD/subjects/tcpdump-tcpdump-4.9.0
export TMP_DIR=$SUBJECT/temp
mkdir $TMP_DIR
# Compile pass and compiler for extracting functions. 
cd $AFLGO/instrument && make && cd -
# Dump all functions.
export FLAGS="-outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export CC="$AFLGO/instrument/fundump-clang $FLAGS"
export LDFLAGS=-lpthread
pushd $SUBJECT
  rm -f $(find . | grep "config.cache")
  ./configure
  make clean
  make
popd
# Check whether Fdumps.txt file is correctly generated.
cat $TMP_DIR/Fdumps.txt
# Turn Fdumps.txt into BBtargets.txt file.
python3 $AFLGO/instrument/fundump2BBtargets.py $TMP_DIR
# Check whether BBtargets.txt file is correctly generated.
cat $TMP_DIR/BBtargets.txt

# Then come into aflgo instrument process.
unset CC CXX
export COPY_FLAGS=$FLAGS
export ADDITIONAL="-targets=$TMP_DIR/BBtargets.txt -outdir=$TMP_DIR -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps"
export FLAGS="$FLAGS $ADDITIONAL"
export CC="$AFLGO/instrument/aflgo-clang $FLAGS"
# Build libxml2 (in order to generate CG and CFGs).
# Meanwhile go have a coffee ☕️
export LDFLAGS=-lpthread
pushd $SUBJECT
  rm -f $(find . | grep "config.cache")
  ./configure
  make clean
  make
popd
# Clean up to avoid distance calculation to fail.
cat $TMP_DIR/BBnames.txt | grep -v "^$"| rev | cut -d: -f2- | rev | sort | uniq > $TMP_DIR/BBnames2.txt && mv $TMP_DIR/BBnames2.txt $TMP_DIR/BBnames.txt
cat $TMP_DIR/BBcalls.txt | grep -Ev "^[^,]*$|^([^,]*,){2,}[^,]*$"| sort | uniq > $TMP_DIR/BBcalls2.txt && mv $TMP_DIR/BBcalls2.txt $TMP_DIR/BBcalls.txt
# Generate distance ☕️
# $AFLGO/distance/gen_distance_orig.sh is the original, but significantly slower, version
$AFLGO/distance/gen_distance_fast.py $SUBJECT $TMP_DIR tcpdump
# Instrument the distances
export FLAGS="$COPY_FLAGS -distance=$TMP_DIR/distance.cfg.txt"
export CC="$AFLGO/instrument/aflgo-clang $FLAGS"
# Clean and build subject with distance instrumentation ☕️
pushd $SUBJECT
  rm -f $(find . | grep "config.cache")
  ./configure
  make clean
  make
popd
```

#### 1 Run

```shell
export AFLPP=<path-to-aflpp>
export TARGET=tcpdump 
export AFLGO=$PWD/aflgo
export DATA_DIR=$PWD/data
export IN_DIR=$DATA_DIR/$TARGET/in
export SUBJECT=$PWD/subjects/tcpdump-tcpdump-4.9.0
mkdir -p $DATA_DIR/$TARGET/outs
# Prepare seed
mkdir -p $IN_DIR
cp $AFLPP/testcases/others/pcap/*.pcap  "$IN_DIR"
timeout 86405s $AFLGO/afl-2.57b/afl-fuzz -z exp -c 45m -i $IN_DIR -o $DATA_DIR/$TARGET/outs/out- $SUBJECT/$TARGET -nr @@
```

