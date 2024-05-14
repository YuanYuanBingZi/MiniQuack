#!/bin/bash
# Compile a Quack program without running it
python3 qklib/quack_parser.py "$1" > OBJ/temp.asm
