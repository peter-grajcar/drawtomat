import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.model.physical import PhysicalObject


class BoxConstraint(Constraint):
    """

    Attributes
    ----------
    obj : PhysicalObject
        an object to which the constraint relates
    box_size : np.ndarray

    """

    def __init__(self, obj: 'PhysicalObject', scale: float = 1.0):
        super().__init__()
        self.obj = obj
        self.box_size = np.array(obj.get_size()) * scale

    def __call__(self, x: 'float', y: 'float') -> bool:
        return (self.obj.x - self.box_size[0] / 2 <= x <= self.obj.x + self.box_size[0] / 2
                and self.obj.y - self.box_size[1] / 2 <= y <= self.obj.y + self.box_size[1] / 2)
