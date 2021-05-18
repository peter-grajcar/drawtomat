from typing import List

import numpy as np

from drawtomat.geometry import lines
from drawtomat.geometry.lines import Line


def inside_polygon(polygon: 'List[np.ndarray]', point: 'np.ndarray') -> bool:
    """
    Determines whether a point is inside a polygon.

    Parameters
    ----------
    polygon
        a set of vertices of a polygon
    point
        a point which is to be determined whether it lies within the polygon.

    Returns
    -------
    bool
        True if the point is inside the polygon.
    """
    intersections = 0
    for i in range(len(polygon)):
        a = np.array(polygon[i - 1])
        b = np.array(polygon[i])
        u = b - a

        (intersection, t) = lines.line_line_intersection_with_t(
            Line(a, u), Line(point, np.array((0, 1)))
        )
        (intersection, s) = lines.line_line_intersection_with_t(
            Line(point, np.array((0, 1))), Line(a, u)
        )
        intersections += t is not None and 0 <= t <= 1 and 0 <= s

    return intersections % 2 == 1
