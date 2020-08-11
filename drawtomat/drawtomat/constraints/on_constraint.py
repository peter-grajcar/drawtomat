import numpy as np

import drawtomat.model.physical
from drawtomat.geometry.rdp import rdp


class OnConstraint:
    """
    On constraint
    """
    def __init__(self, obj: 'drawtomat.model.physical.PhysicalObject', limit=50):
        self.obj = obj
        self.limit = limit

        strokes = quick_draw.get_quickdraw_strokes(self.obj)
        rdp_strokes = [rdp(stroke, 5) for stroke in strokes]

        w, h = obj.get_size()
        is_on_top = (
            lambda point: -0.5
            < (point[1] - obj["position"][1]) / (h * obj["scale"])
            < -0.25
        )
        self.top = [
            point for stroke in rdp_strokes for point in stroke if is_on_top(point)
        ]

    def __call__(self, x: 'float', y: 'float') -> bool:
        # TODO: case for single point
        for i in range(len(self.top)):
            a = self.top[i - 1]
            b = self.top[i]
            if not a[0] <= x <= b[0]:
                continue
            dist_a = (x - a[0]) ** 2 + (y - a[1]) ** 2
            dist_b = (x - b[0]) ** 2 + (y - b[1]) ** 2
            if np.sqrt(dist_a + dist_b) < self.limit:
                return True
        return False
