import numpy as np

import drawtomat.model.physical
from drawtomat.geometry import lines
from drawtomat.geometry.side import Side


class SideConstraint:
    """
    A side constraint.
    """
    def __init__(self, obj: 'drawtomat.model.physical.PhysicalObject', direction=(1, 0)):
        self.obj = obj
        self.direction = np.array(direction)
        self.obj_size = np.array(obj.get_size())

    def __call__(self, x: 'float', y: 'float') -> bool:
        norm_vec = np.array((self.direction[1], -self.direction[0]))

        # choose dominant component of direction vector
        # and set the offset to half the size of the object
        # in the direction of the dominant component
        offset = self.obj_size[np.argmax(abs(self.direction))] / 2

        line = {
            "point": self.obj["position"] + self.direction * offset,
            "vector": norm_vec,
        }
        return lines.get_side_line(line, np.array((x, y))) == Side.RIGHT
