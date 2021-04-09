import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.geometry import lines
from drawtomat.geometry.lines import Line
from drawtomat.model.composition import PhysicalObject


class SideConstraint(Constraint):
    """
    This constraint is satisfied if a point lies on the correct side of a
    half-plane. The half-plane is defined by a point which lies on a boundary
    of a drawing and by a normal vector (perpendicular to the half-plane
    boundary).

    Attributes
    ----------
    obj : PhysicalObject
        An object to which the constraint relates.
    pred: str
        predicate which defines the constraint.
    direction : np.ndarray
        Direction in which the points relative to the object
        will meet the constraint criteria.
    obj_size : np.ndarray
        Size of the object to which the constraint relates.
    """

    def __init__(self, obj: 'PhysicalObject', pred: str, direction=(1, 0), padding=0):
        super().__init__()
        self.obj = obj
        self.pred = pred
        self.direction = np.array(direction)
        self.padding = padding
        self.init()

    def init(self):
        self.obj_size = np.array(self.obj.get_size())

    def __call__(self, xs: 'np.ndarray[float]', ys: 'np.ndarray[float]') -> 'np.ndarray[int]':
        norm_vec = np.array((self.direction[1], -self.direction[0]))

        # choose dominant component of direction vector
        # and set the offset to half the size of the object
        # in the direction of the dominant component
        offset = self.obj_size[np.argmax(abs(self.direction))] / 2 + self.padding

        line = Line(
            np.array(self.obj.get_position()) + self.direction * offset,
            norm_vec
        )
        return lines.get_line_sides(line, xs, ys)
