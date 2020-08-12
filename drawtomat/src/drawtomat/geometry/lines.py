from typing import Tuple, Union

import numpy as np

from drawtomat.geometry.constants import epsilon
from drawtomat.geometry.side import Side


class Line:
    """
    Class representing a line.
    """
    def __init__(self, point: 'np.ndarray', vector: 'np.ndarray'):
        self.point = point
        self.vector = vector


def line_line_intersection_with_t(line_a: 'Line', line_b: 'Line') -> Union[Tuple[None, None], Tuple[np.ndarray, float]]:
    """
    Returns an intersection points of two lines with parameter.

    Parameters
    ----------
    line_a : Line
        First line
    line_b : Line
        Second line

    Returns
    -------
    tuple
        an intersection point of the two lines and parameter
    """
    w = line_a.point - line_b.point
    u = line_a.vector
    v = line_b.vector
    nv = np.array((-v[1], v[0]))

    angle = nv.dot(u)
    if abs(angle - 0) < epsilon:
        return None, None

    t = -nv.dot(w) / angle
    return line_a.point + u * t, t


def line_line_intersection(line_a: 'Line', line_b: 'Line') -> np.ndarray:
    """
    Returns an intersection points of two lines.

    Parameters
    ----------
    line_a : Line
        First line
    line_b : Line
        Second line

    Returns
    -------
    np.ndarray
        an intersection point of the two lines
    """
    return line_line_intersection_with_t[0]


def get_side_line(line: Line, point: 'np.ndarray'):
    """
    Returns a side of a point relative to a line.

    Parameters
    ----------
    line : Line
    point : np.ndarray

    Returns
    -------
    Side
        side of the point
    """
    u = line.vector
    v = point - line.point
    nv = np.array((-v[1], v[0]))
    angle = u.dot(nv)
    return Side.RIGHT if angle < 0 else Side.LEFT


def perp_dist(p0: 'np.ndarray', p1: 'np.ndarray', p2: 'np.ndarray') -> float:
    """
    Perpendicular distance of point p0 from a line defined by points p1 and p2.

    Parameters
    ----------
    p0
        Point
    p1
        First point defining the line
    p2
        Second point defining the line

    Returns
    -------
    float
        distance
    """
    denom = np.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
    num = abs(
        (p2[1] - p1[1]) * p0[0]
        - (p2[0] - p1[0]) * p0[1]
        + p2[0] * p1[1]
        - p2[1] * p1[0]
    )
    return num / denom

