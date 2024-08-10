#!/bin/bash

rm ./*.o
gcc -o child.o child.c
gcc -o fork_wait.o fork_wait.c

./fork_wait.o
