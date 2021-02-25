#!/bin/bash
ORIGINAL_PATH=$(pwd)
QUICKDRAW_PATH=$(pwd)/../quickdraw
VISUALISATION_SCRIPT=$(pwd)/visualisation.py
(cd ../../drawtomat && PYTHONPATH=./src:$QUICKDRAW_PATH python3 $VISUALISATION_SCRIPT "$ORIGINAL_PATH/$1" "$2" "$3")

