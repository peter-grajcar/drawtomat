#!/usr/bin/env python3
import gensim.utils


def read_dataset():
    with open("../conceptualcaptions-dataset/train.txt") as f:
        for i, line in enumerate(f):
            if i % 10000 == 0:
                print(f"{i} lines loaded")

            yield gensim.utils.simple_preprocess(line)


load = True

if load:
    model = gensim.models.KeyedVectors.load(
        "../conceptualcaptions-dataset/train.wv.model"
    )
else:
    documents = list(read_dataset())
    model = gensim.models.Word2Vec(documents, size=150, window=10, iter=10, min_count=2)
    model.train(documents, total_examples=len(documents), epochs=10)
    model.wv.save("../conceptualcaptions-dataset/train.wv.model")
    exit(0)


print("word: ", end="")
word = input()
scores = []
with open("../quickdraw-dataset/categories.txt") as categories:
    for category in categories:
        try:
            score = max([model.similarity(w1=word, w2=cat) for cat in category.split()])
            scores.append(
                {"word": category[:-1], "score": score,}
            )
        except KeyError:
            continue

scores.sort(key=lambda s: -s["score"])
for x in scores[:10]:
    print("{:16s} {:8.4f}".format(x["word"], x["score"]))

