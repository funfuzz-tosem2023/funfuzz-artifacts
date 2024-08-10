#!/bin/bash

# Working at the parent folder of aflpp-edgeonly

# Setup experimental environments
export AFLPP="$PWD/aflpp-edgeonly"   # make
export SCRIPTS="$AFLPP/scripts"
export SEEDS="$AFLPP/testcases"

# Check settings
echo "AFLPP=$AFLPP"
echo "SCRIPTS=$SCRIPTS"
echo "SEEDS=$SEEDS"

# Modify system dump
echo "Modify system dump: echo core > /proc/sys/kernel/core_pattern"
echo "core" > /proc/sys/kernel/core_pattern
