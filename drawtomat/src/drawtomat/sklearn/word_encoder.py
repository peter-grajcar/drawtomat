import fasttext
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class WordEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, filename):
        self.filename = filename
        self.model = fasttext.load_model(self.filename)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["model"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.model = fasttext.load_model(self.filename)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return np.array([np.concatenate([self.model[w] for w in x]) for x in X])

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)
