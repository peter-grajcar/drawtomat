from typing import List

import numpy as np


def triangle_area(triangle: 'List[np.ndarray]') -> 'float':
    """
    Computes the area of a triangle.

    Parameters
    ----------
    triangle : 'List[np.ndarray]'
        triangle

    Returns
    -------
    float
        area of the triangle
    """
    u = triangle[1] - triangle[0]
    v = triangle[2] - triangle[0]
    return 0.5 * np.sqrt(u.dot(u) * v.dot(v) - u.dot(v) ** 2)
