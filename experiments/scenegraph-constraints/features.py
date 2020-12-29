import fasttext
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin

class WordEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, filename):
        self.filename = filename
        self.model = fasttext.load_model(self.filename)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return np.array([np.concatenate([self.model[w] for w in x]) for x in X])

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)


column_transformer = ColumnTransformer(
    [
        ("word_encoder", WordEncoder("../word2vec/conceptual-captions-fasttext.model"), [0, 1]), 
        ("predicate_encoder", OneHotEncoder(), [2])
    ],
    remainder='passthrough'
)


