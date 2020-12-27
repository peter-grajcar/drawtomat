#!/usr/bin/env python3
from fasttext_embedding import *

embedding = Embedding("conceptual-captions-fasttext.model")

word = input("word: ")
similarity = []
for category in embedding.categories:
    sim = cos_sim(embedding.model[word], embedding.model[category])
    similarity.append((category, sim))

similarity.sort(key=lambda tup: -tup[1])
for best in similarity[:10]:
    print(best)

