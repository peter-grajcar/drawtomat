from typing import List

import numpy as np

from drawtomat.geometry import polygons
from drawtomat.geometry.rdp import rdp
from drawtomat.model.physical import PhysicalObject


class InsideConstraint:
    """
    Inside constraint.

    Attributes
    ----------
    obj : PhysicalObject
        an object to which the constraint relates
    rdp_strokes : List[np.ndarray]
        object strokes reduced by RDP algorithm

    See Also
    --------
    ~drawtomat.geometry.rdp
    """
    def __init__(self, obj: 'PhysicalObject'):
        self.obj = obj

        cx, cy = obj.get_centre()
        strokes = [
            [
                (x + obj.x - cx, y + obj.y - cy) for x, y in zip(stroke[0], stroke[1])
            ] for stroke in obj.strokes
        ]

        self.rdp_strokes = [rdp(stroke, 10) for stroke in strokes]

    def __call__(self, x: 'float', y: 'float') -> bool:
        for stroke in self.rdp_strokes:
            if polygons.inside_polygon(stroke, np.array((x, y))):
                return True
        return False
