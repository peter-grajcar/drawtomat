from typing import List

import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.model.physical import PhysicalObject


class DisjunctionConstraint(Constraint):
    """
    Disjunction constraint. This constraint is satisfied whenever at least one
    of the constraints is satisfied.

    Attributes
    ----------
    constraints : List[Constraint]
        object strokes reduced by RDP algorithm
    """

    def __init__(self, obj: 'PhysicalObject', constraints: 'List[Constraint]'):
        super().__init__()
        self.obj = obj
        self.constraints = constraints

    def init(self):
        pass

    def __call__(self, xs: 'np.ndarray[float]', ys: 'np.ndarray[float]') -> 'np.ndarray[int]':
        result = np.zeros(shape=xs.shape[0])
        for constraint in self.constraints:
            result += constraint(xs, ys)
        return result > 0
