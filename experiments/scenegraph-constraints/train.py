#!/usr/bin/env python3
import sys
import json
import pickle
import fasttext
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.utils import shuffle

class WordEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, filename):
        self.filename = filename

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        model = fasttext.load_model(self.filename)
        return np.array([np.concatenate([model[w] for w in x]) for x in X])

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)


column_transformer = ColumnTransformer(
    [
        # ("word_encoder", WordEncoder("../word2vec/conceptual-captions-fasttext.model"), [0]), 
        ("predicate_encoder", OneHotEncoder(), [0])
    ],
    remainder=StandardScaler(),
    verbose=True
)

model = MLPClassifier(max_iter=100, tol=1e-6, hidden_layer_sizes=(100), verbose=True, warm_start=True)

pipeline = Pipeline(steps=[
        ("transformer", column_transformer),
        ("classifier", model)
    ],
    verbose=True
)

with open("train.data", "rb") as f:
    X, t = pickle.load(f)

column_transformer.fit(X)

X, t = shuffle(X, t)
size = 100000
for i in range(0, len(X), size):
    print(i)
    model.partial_fit(column_transformer.transform(X[i:i+size]), t[i:i+size], classes=[0, 1])

with open("scenegraph-constraints.model", "wb") as f:
    pickle.dump(pipeline, f)

