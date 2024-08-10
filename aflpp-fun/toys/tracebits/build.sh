#!/bin/bash

# First clean
bash ./clean.sh

# -c: compile but not link
gcc -o rt.o -c rt.c
#gcc -Wall -Wextra -g -o PUT PUT.c rt.o
gcc -o PUT PUT.c rt.o
gcc fuzzer.c -o fuzzer

gcc getenv.c -o getenv.o
gcc setenv.c -o setenv.o
gcc fork_env.c -o fork_env.o
