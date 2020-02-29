#!/bin/bash

cat quickdraw-dataset/categories.txt | xargs -I {} sh -c "python3 experiments/quickdraw-dataset-extract.py --name=\"{}\" > quickdraw-dataset/dataset/\"{}\".ndjson"