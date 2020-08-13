from drawtomat.constraints import Constraint
from drawtomat.geometry import lines
from drawtomat.geometry.rdp import rdp
from drawtomat.model.physical import PhysicalObject


class OnConstraint(Constraint):
    """
    On constraint.

    Attributes
    ----------
    obj : PhysicalObject
        an object to which the constraint relates
    limit : float
        maximal distance from the lines on the top
    """

    def __init__(self, obj: 'PhysicalObject', limit: 'float' = 10):
        super().__init__()
        self.obj = obj
        self.limit = limit

        strokes = [
            [
                (x + obj.x, y + obj.y) for x, y in zip(stroke[0], stroke[1])
            ] for stroke in obj.strokes
        ]
        rdp_strokes = [rdp(stroke, 5) for stroke in strokes]

        is_on_top = (
            lambda point: (point[1] - obj.y) / obj.get_height() < -0.25
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
            if abs(lines.perp_dist((x, y), a, b)) < self.limit:
                return True
        return False
