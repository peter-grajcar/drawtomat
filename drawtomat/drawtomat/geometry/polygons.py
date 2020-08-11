from typing import List

import numpy as np

from drawtomat.geometry import lines


def inside_polygon(polygon: 'List[np.ndarray]', point: 'np.ndarray') -> bool:
    """

    Parameters
    ----------
    polygon
    point

    Returns
    -------

    """
    intersections = 0
    for i in range(len(polygon)):
        a = np.array(polygon[i - 1])
        b = np.array(polygon[i])
        u = b - a

        (intersection, t) = lines.line_line_intersection_with_t(
            {"point": a, "vector": u}, {"point": point, "vector": np.array((1, 0))}
        )
        # not ideal, TODO:
        (intersection, s) = lines.line_line_intersection_with_t(
            {"point": point, "vector": np.array((1, 0))}, {"point": a, "vector": u}
        )
        intersections += t is not None and 0 <= t <= 1 and 0 <= s

    return intersections % 2 == 1

