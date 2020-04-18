import numpy as np

from drawtomat.geometry.constants import epsilon


class Line:
    def __init__(self, point: 'np.ndarray', vector: 'np.ndarray'):
        self.point = point
        self.vector = vector


def line_line_intersection(line_a: 'Line', line_b: 'Line'):
    """

    Parameters
    ----------
    line_a
    line_b

    Returns
    -------

    """
    w = line_a.point - line_b.point
    u = line_a.vector
    v = line_b.vector
    nv = np.array((-v[1], v[0]))

    angle = nv.dot(u)
    if abs(angle - 0) < epsilon:
        return None

    t = -nv.dot(w) / angle
    return line_a["point"] + u * t


def mean_intersection(lines: 'list'):
    """

    Parameters
    ----------
    lines

    Returns
    -------

    """
    return np.mean([
        line_line_intersection(a, b) for a in lines for b in lines if a is not b
    ], axis=0)
