#!/usr/bin/env python3
import sys

data = []

def to_float(s):
    if not s:
        return .0
    return float(s)

def ratio(a, b):
    if b == 0:
        return ""
    return a / b

for line in sys.stdin:
    cols = line.strip().split(",")
    data.append((cols[0], to_float(cols[1]), to_float(cols[2])))

for a in data:
    for b in data:
        r1 = ratio(a[1], b[1])
        r2 = ratio(a[2], b[2])
        if r1 or r2:
            print(a[0], b[0], r1, r2, sep=",")

