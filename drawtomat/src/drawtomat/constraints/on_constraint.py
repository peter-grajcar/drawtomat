import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.geometry import lines
from drawtomat.geometry.rdp import rdp
from drawtomat.model.composition import PhysicalObject


class OnConstraint(Constraint):
    """
    This constraint takes all line segments in the top 25% of a drawing. If the
    square distance of a point is within a specified limit the constraint is
    satisfied.

    Attributes
    ----------
    obj : PhysicalObject
        An object to which the constraint relates.
    pred: str
        Predicate which defines the constraint.
    limit : float
        Maximal distance from the lines on the top.
    """

    def __init__(self, obj: 'PhysicalObject', pred: 'str', limit: 'float' = 10):
        super().__init__()
        self.obj = obj
        self.pred = pred
        self.limit = limit
        self.init()

    def init(self):
        strokes = [
            [
                (x + self.obj.x, y + self.obj.y) for x, y in zip(stroke[0], stroke[1])
            ] for stroke in self.obj.strokes
        ]
        rdp_strokes = [rdp(stroke, 5) for stroke in strokes]

        is_on_top = (
            lambda point: (point[1] - self.obj.y) / self.obj.get_height() < -0.25
        )
        self.top = [
            point for stroke in rdp_strokes for point in stroke if is_on_top(point)
        ]

    def _is_on(self, x: 'float', y: 'float') -> 'int':
        for i in range(len(self.top)):
            a = self.top[i - 1]
            b = self.top[i]
            if not a[0] <= x <= b[0]:
                continue

            dist_a = (x - a[0]) ** 2 + (y - a[1]) ** 2
            dist_b = (x - b[0]) ** 2 + (y - b[1]) ** 2
            if abs(lines.perp_dist((x, y), a, b)) < self.limit:
                return 1
        return 0

    def __call__(self, xs: 'np.ndarray[float]', ys: 'np.ndarray[float]') -> 'np.ndarray[int]':
        return np.array([self._is_on(x, y) for x, y in zip(xs, ys)])
