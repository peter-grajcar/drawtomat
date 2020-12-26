#!/usr/bin/env python3
import fasttext
import numpy as np


def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


model = fasttext.load_model("conceptual-captions-fasttext.model")

categories = []
with open("../../quickdraw-dataset/categories.txt") as f:
    for category in f:
        categories.append(category.strip())

word = input("word: ")
similarity = []
for category in categories:
    sim = cos_sim(model[word], model[category])
    similarity.append((category, sim))

similarity.sort(key=lambda tup: -tup[1])
for best in similarity[:10]:
    print(best)

