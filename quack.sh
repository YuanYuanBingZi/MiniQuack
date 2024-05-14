#!/bin/bash
# Compile and run a Quack program
python3 qklib/quack_parser.py "$1" > OBJ/temp.asm
python3 qklib/vm.py OBJ/temp.asm