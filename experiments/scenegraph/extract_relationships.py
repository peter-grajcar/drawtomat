#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    data = json.loads(line)
    for rel in data["relationships"]:
        print(json.dumps(rel))

