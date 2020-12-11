import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.geometry import lines
from drawtomat.geometry.lines import Line
from drawtomat.geometry.side import Side
from drawtomat.model.physical import PhysicalObject


class SideConstraint(Constraint):
    """
    A side constraint.

    Attributes
    ----------
    obj : PhysicalObject
        an object to which the constraint relates
    direction : np.ndarray
        direction in which the points relative to the object
        will meet the constraint criteria
    obj_size : np.ndarray
        size of the object to which the constraint relates.
    """
    def __init__(self, obj: 'PhysicalObject', direction=(1, 0), padding=0):
        super().__init__()
        self.obj = obj
        self.direction = np.array(direction)
        self.padding = padding
        self.init()

    def init(self):
        self.obj_size = np.array(self.obj.get_size())

    def __call__(self, x: 'float', y: 'float') -> bool:
        norm_vec = np.array((self.direction[1], -self.direction[0]))

        # choose dominant component of direction vector
        # and set the offset to half the size of the object
        # in the direction of the dominant component
        offset = self.obj_size[np.argmax(abs(self.direction))] / 2 + self.padding

        line = Line(
            np.array(self.obj.get_position()) + self.direction * offset,
            norm_vec
        )
        return lines.get_side_line(line, np.array((x, y))) == Side.RIGHT
