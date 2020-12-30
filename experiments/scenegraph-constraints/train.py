#!/usr/bin/env python3
import sys
import json
import features
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
import pickle

with open("predicates.txt") as f:
    predicates = {line.strip() for line in f}

spinner = ["-", "\\", "|", "/"]
counter = 0
relationships = []
for line in sys.stdin:
    counter += 1
    if counter % 100 == 99:
        print(spinner[(counter // 100) % 4], counter + 1, end="\r")
    
    relationships.append(json.loads(line))

print()

rel_count = len(relationships)

def dist(x1, y1, x2, y2):
    fst = not x1 and not y1
    snd = not x2 and not y2
    if fst and snd:
        return 1
    elif fst or snd:
        return 0
    return (x1*x2 + y1*y2) / (np.sqrt(x1*x1 + y1*y1) * np.sqrt(x2*x2 + y2*y2))

X = []
t = []

counter = 0
for data in relationships:
    counter += 1
    if counter % 100 == 99:
        print(spinner[(counter // 100) % 4], counter + 1, end="\r")
    
    pred = data["predicate"].upper()

    if not pred in predicates:
        continue

    sub = data["subject"]
    obj = data["object"]
    
    dx = ((sub["x"] + sub["w"]/2) - (obj["x"] + obj["w"]/2)) / obj["w"]
    dy = ((sub["y"] + sub["h"]/2) - (obj["y"] + obj["h"]/2)) / obj["h"]
    
    X.append([obj["name"], pred, dx, dy])
    t.append(1)

    wrong = None
    while wrong is None or wrong["predicate"] == pred or dist(wrong_dx, wrong_dy, dx, dy) > 0.8:
        wrong = relationships[np.random.randint(low=0, high=rel_count)]
        wrong_sub = wrong["subject"]
        wrong_obj = wrong["object"]
        wrong_dx = ((wrong_sub["x"] + wrong_sub["w"]/2) - (wrong_obj["x"] + wrong_obj["w"]/2)) / obj["w"]
        wrong_dy = ((wrong_sub["y"] + wrong_sub["h"]/2) - (wrong_obj["y"] + wrong_obj["h"]/2)) / obj["h"]

    X.append([obj["name"], pred, wrong_dx, wrong_dy])
    t.append(0)

print()

pipeline = Pipeline(steps=[
    ("transformer", features.column_transformer),
    ("classifier", MLPClassifier(hidden_layer_sizes=(300, 50), max_iter=500, verbose=True))
    ])


pipeline.fit(X, t)

with open("scenegraph-constraints.model", "wb") as f:
    pickle.dump(pipeline, f)

