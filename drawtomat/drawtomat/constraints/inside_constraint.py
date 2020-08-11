import numpy as np

import drawtomat.model.physical
from drawtomat.geometry import polygons
from drawtomat.geometry.rdp import rdp


class inside_constraint:
    def __init__(self, obj: 'drawtomat.model.physical.PhysicalObject'):
        self.obj = obj
        strokes = quick_draw.get_quickdraw_strokes(self.obj)
        self.rdp_strokes = [rdp(stroke, 10) for stroke in strokes]

    def __call__(self, x: 'float', y: 'float') -> bool:
        for stroke in self.rdp_strokes:
            if polygons.inside_polygon(stroke, np.array((x, y))):
                return True
        return False
