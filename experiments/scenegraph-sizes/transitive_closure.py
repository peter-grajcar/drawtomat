#!/usr/bin/env python3
import sys
import numpy as np

categories = []
indices = {}
with open("../../quickdraw-dataset/categories.txt") as f:
    for i, line in enumerate(f):
        categories.append(line.strip())
        indices[line.strip()] = i

n = len(categories)
rel = np.zeros(shape=(n, n))

for line in sys.stdin:
    sub, obj, w, h = line.split(",")
    i = indices[sub]
    j = indices[obj]
    rel[i,j] = float(w)

nonzeros = np.count_nonzero(rel)
print(nonzeros, end="\r", file=sys.stderr)

new = nonzeros != n*n
while new:
    print("iteration", file=sys.stderr)
    new = False

    tmp = np.copy(rel)
    for i in range(n):
        for j in range(n):
            if rel[i, j]:
                continue

            rel_count = 0
            rel_sum = 0
            for k in range(n):
                if rel[i, k] and rel[k, j]:
                    rel_sum += rel[i, k] * rel[k, j]
                    rel_count += 1
            
            if rel_count:
                tmp[i, j] = rel_sum / rel_count
                nonzeros += 1
                new = True
                
                if nonzeros % 100 == 0:
                    print(nonzeros, end="\r", file=sys.stderr)

    rel = np.copy(tmp)

print(np.count_nonzero(rel), file=sys.stderr)

for i in range(n):
    for j in range(n):
        if rel[i, j]:
            print(categories[i], categories[j], rel[i, j], 0, sep=",")

