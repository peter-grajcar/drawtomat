import pickle

import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.model.physical import PhysicalObject

with open("resources/sklearn/constraints.model", "rb") as f:
    model = pickle.load(f)


class SklearnConstraint(Constraint):
    """
    # TODO
    """

    def __init__(self, obj: 'PhysicalObject', pred: 'str'):
        super().__init__()
        self.obj = obj
        self.pred = pred
        self.init()

    def init(self):
        pass

    def __call__(self, x: 'np.ndarray', y: 'np.ndarray') -> 'np.ndarray[int]':
        preds = np.full(shape=(x.shape[0]), fill_value=self.pred)
        dx = (x - self.obj.get_position()[0]) / self.obj.get_width()
        dy = (y - self.obj.get_position()[1]) / self.obj.get_height()
        data = np.column_stack((preds, dx, dy))
        return model.predict(data)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pred}, {self.obj.entity.word})"
