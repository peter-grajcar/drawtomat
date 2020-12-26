#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    data = json.loads(line)
    for obj in data["objects"]:
        print(json.dumps(obj))

