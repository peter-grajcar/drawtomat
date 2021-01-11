#!/bin/bash

ls -1 output/attributes_*relative*.csv | xargs -I{} bash -c "wc -l {} && ./eval.py output/attributes_manual_relative.csv {}"

