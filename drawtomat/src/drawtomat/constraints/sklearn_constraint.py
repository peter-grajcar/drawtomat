import pickle

import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.model.composition import PhysicalObject


class SklearnConstraint(Constraint):
    """
    Constraint which uses Multi Layered Perceptron (MLP) binary classifier to
    determine whether a set of points match given predicate.

    Attributes
    ----------
    obj : PhysicalObject
        an object to which the constraint relates
    pred: str
        predicate which defines the constraint
    """

    _model = None

    @staticmethod
    def _get_model():
        if SklearnConstraint._model is None:
            with open("resources/sklearn/constraints.model", "rb") as f:
                SklearnConstraint._model = pickle.load(f)
        return SklearnConstraint._model

    def __init__(self, obj: 'PhysicalObject', pred: 'str'):
        super().__init__()
        self.obj = obj
        self.pred = pred
        self.init()

    def init(self):
        pass

    def __call__(self, x: 'np.ndarray', y: 'np.ndarray') -> 'np.ndarray[int]':
        objs = np.full(shape=(x.shape[0]), fill_value=self.obj.entity.word)
        preds = np.full(shape=(x.shape[0]), fill_value=self.pred)
        dx = (x - self.obj.get_position()[0]) / self.obj.get_width()
        dy = (y - self.obj.get_position()[1]) / self.obj.get_height()
        data = np.column_stack((objs, preds, dx, dy))
        return self._get_model().predict(data)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pred}, {self.obj.entity.word})"
