#!/bin/bash

TEST_NAME=testdcc

echo "AFL_FUN_TEMP=$AFL_FUN_TEMP"
gcc -o "$TEST_NAME".o "$TEST_NAME".c && ./"$TEST_NAME".o "$AFL_FUN_TEMP"
