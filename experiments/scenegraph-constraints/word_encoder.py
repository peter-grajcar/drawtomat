import fasttext
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

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


