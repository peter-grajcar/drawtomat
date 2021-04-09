import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.model.composition import PhysicalObject


class BoxConstraint(Constraint):
    """
    Box constraint is satisfied if a point lies in a bounding box of a drawing.
    The bounding box can also be scaled.

    Attributes
    ----------
    obj : PhysicalObject
        An object to which the constraint relates.
    pred: str
        Predicate which defines the constraint.
    box_size : np.ndarray
        Scaled size of the box (width, height).
    """

    def __init__(self, obj: 'PhysicalObject', pred: 'str', scale: float = 1.0):
        super().__init__()
        self.obj = obj
        self.pred = pred
        self.box_size = np.array(obj.get_size()) * scale

    def __call__(self, xs: 'np.ndarray[float]', ys: 'np.ndarray[float]') -> 'np.ndarray[int]':
        return ((self.obj.x - self.box_size[0] / 2 <= xs)
                & (xs <= self.obj.x + self.box_size[0] / 2)
                & (self.obj.y - self.box_size[1] / 2 <= ys)
                & (ys <= self.obj.y + self.box_size[1] / 2))
