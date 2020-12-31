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
        ("word_encoder", WordEncoder("../word2vec/conceptual-captions-fasttext.model"), [0]), 
        ("predicate_encoder", OneHotEncoder(), [1])
    ],
    remainder=StandardScaler(),
    verbose=True
)

pipeline = Pipeline(steps=[
    ("transformer", column_transformer),
    ("classifier", MLPClassifier(hidden_layer_sizes=(300, 50), max_iter=500, verbose=True))
    ],
    verbose=True
)


with open("train.data", "rb") as f:
    X, t = pickle.load(f)

pipeline.fit(X, t)

with open("scenegraph-constraints.model", "wb") as f:
    pickle.dump(pipeline, f)

