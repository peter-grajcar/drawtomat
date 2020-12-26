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
    if sub in quickdraw and obj in quickdraw:
        key = f"{sub},{obj}"
        sizes[key]["count"] += 1
        sizes[key]["sum_w"] += data["subject"]["w"] / data["object"]["w"]
        sizes[key]["sum_h"] += data["subject"]["h"] / data["object"]["h"]
    # print(f"{pred}({sub},{obj})")

for key, value in sizes.items():
    print(value["count"], file=sys.stderr)
    w = value["sum_w"] / value["count"]
    h = value["sum_h"] / value["count"]
    sub, obj = key.split(",")
    if not f"{obj},{sub}" in sizes:
        print(f"{obj},{sub},{1/w},{1/h}")
    print(f"{sub},{obj},{w},{h}")

