#!/usr/bin/env python3
import sys

sys.path.insert(0, "../word2vec/")

import json
from collections import defaultdict
from fasttext_embedding import Embedding

embedding = Embedding("../word2vec/conceptual-captions-fasttext.model")
similar_words = {}

sizes = defaultdict(lambda: { "count": 0, "sum_w": 0, "sum_h": 0 })

threshold = 0.85
counter = 0

for line in sys.stdin:
    counter += 1
    if counter % 100 == 99:
        print(counter + 1, file=sys.stderr, end="\r")
    
    data = json.loads(line)
    pred = data["predicate"].upper().replace(" ", "_")
    
    sub_name = data["subject"]["name"]
    obj_name = data["object"]["name"]

    if sub_name in similar_words:
        sub, sim = similar_words[sub_name]
        if sim < threshold:
            continue
    else:
        sub, sim = embedding.most_similar(sub_name, include_similarity=True)
        similar_words[sub_name] = (sub, sim)
        if sim < threshold:
            continue

    if obj_name in similar_words:
        obj, sim = similar_words[obj_name]
        if sim < threshold:
            continue
    else:
        obj, sim = embedding.most_similar(obj_name, include_similarity=True)
        similar_words[obj_name] = (obj, sim)
        if sim < threshold:
            continue
        
    key = f"{sub},{obj}"
    sizes[key]["count"] += 1
    sizes[key]["sum_w"] += data["subject"]["w"] / data["object"]["w"]
    sizes[key]["sum_h"] += data["subject"]["h"] / data["object"]["h"]
    # print(f"{pred}({sub},{obj})")


for key, value in sizes.items():
    # print(value["count"], file=sys.stderr)
    w = value["sum_w"] / value["count"]
    h = value["sum_h"] / value["count"]
    sub, obj = key.split(",")
    if not f"{obj},{sub}" in sizes:
        print(f"{obj},{sub},{1/w},{1/h}")
    print(f"{sub},{obj},{w},{h}")
