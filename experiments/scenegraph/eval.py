#!/usr/bin/env python3
import numpy as np
import sys

attrs_a = {}
attrs_b = {}

def to_float(s):
    if not s:
        return .0
    return float(s)

with open(sys.argv[1]) as f:
    for line in f:
        cols = line.strip().split(",")
        attrs_a[f"{cols[0]},{cols[1]}"] = (to_float(cols[2]), to_float(cols[3]))

with open(sys.argv[2]) as f:
    for line in f:
        cols = line.strip().split(",")
        attrs_b[f"{cols[0]},{cols[1]}"] = (to_float(cols[2]), to_float(cols[3]))

n_w = 0
n_h = 0
mse_w = 0
mse_h = 0

for key, ratio_a in attrs_a.items():
    if key in attrs_b:
        ratio_b = attrs_b[key]
        if ratio_a[0] and ratio_b[0]:
            mse_w += (ratio_a[0] - ratio_b[0])**2
            n_w += 1
        if ratio_a[1] and ratio_b[1]:
            mse_h += (ratio_a[1] - ratio_b[1])**2
            n_h += 1

mse_w /= n_w
mse_h /= n_h

print("width RMSE =", np.sqrt(mse_w))
print("height RMSE =", np.sqrt(mse_h))

