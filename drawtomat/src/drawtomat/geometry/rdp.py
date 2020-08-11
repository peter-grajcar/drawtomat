from typing import List, Tuple

import numpy as np

from drawtomat.geometry import lines


def rdp(points: 'List[Tuple[float, float]]', epsilon: 'float') -> List[np.ndarray]:
    """
    Ramer–Douglas–Peucker algorithm.

    Parameters
    ----------
    points : list
        a list of points
    epsilon
        epsilon value

    Returns
    -------
    list
        a reduced list of points
    """
    stack = [(0, len(points))]
    result_stack = []

    while stack:
        op = stack.pop()
        if op == "merge":
            r1 = result_stack.pop()
            r2 = result_stack.pop()
            result_stack.append(r1 + r2)
            continue
        start, end = op

        dmax = 0
        index = 0
        for i in range(start + 1, end - 2):
            d = lines.perp_dist(points[i], points[start], points[end - 1])
            if d > dmax:
                dmax = d
                index = i

        if dmax > epsilon:
            stack.append("merge")
            stack.append((start, index))
            stack.append((index, end))
        else:
            result_stack.append([points[start], points[end - 1]])

    return result_stack[0]
