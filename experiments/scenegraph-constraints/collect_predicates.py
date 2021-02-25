#!/usr/bin/env python3
import sys
import json
from collections import defaultdict

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} <limit>")
    exit(1)

limit = int(sys.argv[1])
predicates = defaultdict(int)

for line in sys.stdin:
    data = json.loads(line)
    pred = data["predicate"].upper()
    if pred.endswith(" A"):
        pred = pred[:-2]
    predicates[pred] += 1

sorted_predicates = sorted([(pred, count) for pred, count in predicates.items() if count > limit], key=lambda x: -x[1])
for pred, count in sorted_predicates[:limit]:
    print(pred)

