#!/usr/bin/env python3
from nltk.corpus import wordnet
from pprint import pprint

words = [
    "big",
    "red",
    "small",
    "large",
    "green",
    "purple",
    "tiny",
    "gigantic",
    "maroon",
    "indigo",
    "wide",
    "narrow",
    "tall",
    "short",
    "long",
]
attributes = {}

print("Original list of attributes:")
print(words)
print()
print("Sorted attributes:")

chromatic = wordnet.synset("chromatic.a.03")
colored = wordnet.synset("colored.a.01")
size = wordnet.synset("size.n.01")
width = wordnet.synset("width.n.01")
height = wordnet.synset("stature.n.02")


def is_attr(synset, attr):
    if attr in synset.attributes():
        return True
    if attr in synset.similar_tos():
        return True
    for sim in synset.similar_tos():
        if attr in sim.attributes():
            return True
    return False


for word in words:
    synsets = wordnet.synsets(word, wordnet.ADJ)
    # print(synset.attributes())
    for synset in synsets:
        if is_attr(synset, chromatic) or is_attr(synset, colored):
            if attributes.get("color"):
                attributes["color"].append(word)
            else:
                attributes["color"] = [word]
            break
        elif is_attr(synset, size):
            if attributes.get("size"):
                attributes["size"].append(word)
            else:
                attributes["size"] = [word]
            break
        elif is_attr(synset, width):
            if attributes.get("width"):
                attributes["width"].append(word)
            else:
                attributes["width"] = [word]
            break
        elif is_attr(synset, height):
            if attributes.get("height"):
                attributes["height"].append(word)
            else:
                attributes["height"] = [word]
            break

pprint(attributes)
