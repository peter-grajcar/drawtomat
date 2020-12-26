#!/usr/bin/env python3
import sys
import json
from collections import defaultdict

with open("../../quickdraw-dataset/categories.txt") as f:
    quickdraw = [category.strip() for category in f]

sizes = defaultdict(lambda: { "count": 0, "sum_w": 0, "sum_h": 0 })

for line in sys.stdin:
    data = json.loads(line)
    pred = data["predicate"].upper().replace(" ", "_")
    sub = data["subject"]["name"]
    obj = data["object"]["name"]
    if sub in quickdraw:
        sizes[sub]["count"] += 1
        sizes[sub]["sum_w"] += data["subject"]["w"]
        sizes[sub]["sum_h"] += data["subject"]["h"]
    if obj in quickdraw:
        sizes[obj]["count"] += 1
        sizes[obj]["sum_w"] += data["object"]["w"]
        sizes[obj]["sum_h"] += data["object"]["h"]
    
    # print(f"{pred}({sub},{obj})")

for key, value in sizes.items():
    w = value["sum_w"] / value["count"]
    h = value["sum_h"] / value["count"]
    print(f"{key};{w:.0f};{h:.0f}")

