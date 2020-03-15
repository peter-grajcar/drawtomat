#!/bin/bash

cat quickdraw-dataset/categories.txt | xargs -I {} sh -c "python3 experiments/quickdraw-dataset-extract.py --count=10000 --name=\"{}\" > quickdraw-dataset/dataset/\"{}\".ndjson"