#!/bin/bash

rm -f ./*.o

gcc -o PUT.o PUT.c rt.c
gcc -o fuzzer.o fuzzer.c
