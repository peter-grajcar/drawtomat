from typing import List

import numpy as np


def triangle_area(triangle: 'List[np.ndarray]') -> 'float':
    u = triangle[1] - triangle[0]
    v = triangle[2] - triangle[0]
    return 0.5 * np.sqrt(u.dot(u) * v.dot(v) - u.dot(v) ** 2)
