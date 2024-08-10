#!/bin/bash

rm ./*.o

gcc -o srvstdout.o srvstdout.c

./srvstdout.o | python3 cltstdin.py
