#!/usr/bin/env python3
import sys
import json
import pickle
import fasttext
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.utils import shuffle
from drawtomat.sklearn.word_encoder import WordEncoder

if len(sys.argv) < 3:
    print("usage: train <input data> <output model>")
    exit(1)

column_transformer = ColumnTransformer(
    [
        ("word_encoder", WordEncoder("resources/fasttext/conceptual-captions-fasttext.model"), [0]), 
        ("predicate_encoder", OneHotEncoder(), [1])
    ],
    remainder=StandardScaler(),
    verbose=True
)

model = MLPClassifier(max_iter=100, tol=1e-6, hidden_layer_sizes=(300, 200, 100), verbose=True, warm_start=True)

pipeline = Pipeline(steps=[
        ("transformer", column_transformer),
        ("classifier", model)
    ],
    verbose=True
)

with open(sys.argv[1], "rb") as f:
    X, t = pickle.load(f)

X = column_transformer.fit_transform(X)

size = 250000

for j in range(2):
    X, t = shuffle(X, t)
    for i in range(0, X.shape[0], size):
        print(i)
        model.partial_fit(X[i:i+size], t[i:i+size], classes=[0, 1])

with open(sys.argv[2], "wb") as f:
    pickle.dump(pipeline, f)

