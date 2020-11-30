from typing import List

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

    def __call__(self, x: 'float', y: 'float') -> bool:
        for constraint in self.constraints:
            if constraint(x, y):
                return True
        return False
