#!/bin/bash
DATA=$(pwd)/data/train.data
MODEL=$(pwd)/models/scenegraph-constraints.model
TRAIN_SCRIPT=$(pwd)/train.py
(cd ../../drawtomat && PYTHONPATH=./src python3 $TRAIN_SCRIPT $DATA $MODEL)

