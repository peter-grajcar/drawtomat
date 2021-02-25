from typing import List

import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.geometry import polygons
from drawtomat.geometry.rdp import rdp
from drawtomat.model.composition import PhysicalObject


class InsideConstraint(Constraint):
    """
    Inside constraint.

    Attributes
    ----------
    obj : PhysicalObject
        An object to which the constraint relates.
    pred: str
        Predicate which defines the constraint.
    rdp_strokes : List[np.ndarray]
        Object strokes reduced by RDP algorithm.

    See Also
    --------
    drawtomat.geometry.rdp
    """

    def __init__(self, obj: 'PhysicalObject', pred: 'str'):
        super().__init__()
        self.obj = obj
        self.pred = pred
        self.rdp_strokes = []
        self.init()

    def init(self):
        strokes = [
            [
                (x + self.obj.x, y + self.obj.y) for x, y in zip(stroke[0], stroke[1])
            ] for stroke in self.obj.strokes
        ]
        self.rdp_strokes = [rdp(stroke, max(self.obj.get_size()) / 4) for stroke in strokes]

    def _is_inside(self, x: 'float', y: 'float') -> int:
        for stroke in self.rdp_strokes:
            if polygons.inside_polygon(stroke, np.array((x, y))):
                return 1
        return 0

    def __call__(self, xs: 'np.ndarray[float]', ys: 'np.ndarray[float]') -> 'np.ndarray[int]':
        return np.array([self._is_inside(x, y) for x, y in zip(xs, ys)])
