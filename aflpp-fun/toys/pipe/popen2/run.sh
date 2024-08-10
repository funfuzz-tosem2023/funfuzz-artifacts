#!/bin/bash

rm ./*.o

gcc -o server.o server.c

./server.o
