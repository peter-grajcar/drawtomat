#!/usr/bin/env python3
import sys
import json
import features

with open("predicates.txt") as f:
    predicates = {line.strip() for line in f}

X = []

for line in sys.stdin:
    data = json.loads(line)

    pred = data["predicate"].upper()

    if not pred in predicates:
        continue

    sub = data["subject"]
    obj = data["object"]
    
    dx = ((sub["x"] + sub["w"]/2) - (obj["x"] + obj["w"]/2)) / obj["w"]
    dy = ((sub["y"] + sub["h"]/2) - (obj["y"] + obj["h"]/2)) / obj["h"]
    
    X.append([sub["name"], obj["name"], pred, dx, dy])

train_data = features.column_transformer.fit_transform(X)
print(train_data.shape)

