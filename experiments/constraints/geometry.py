import numpy as np

epsilon = 1e-8


def get_side_line(line, point):
    u = line["vector"]
    v = point - line["point"]
    nv = np.array((-v[1], v[0]))
    angle = u.dot(nv)
    return "R" if angle < 0 else "L"


# returns side of point p3 with respect to line p1,p2
def get_side(p1, p2, p3):
    sign = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
    return "R" if sign < 0 else "L"


def perp_dist(p0, p1, p2):
    denom = np.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
    num = abs(
        (p2[1] - p1[1]) * p0[0]
        - (p2[0] - p1[0]) * p0[1]
        + p2[0] * p1[1]
        - p2[1] * p1[0]
    )
    return num / denom


def line_line_intersection_with_t(line_a, line_b):
    w = line_a["point"] - line_b["point"]
    u = line_a["vector"]
    v = line_b["vector"]
    nv = np.array((-v[1], v[0]))

    angle = nv.dot(u)
    if abs(angle - 0) < epsilon:
        return (None, None)

    t = -nv.dot(w) / angle
    return (line_a["point"] + u * t, t)


def line_line_intersection(line_a, line_b):
    return line_line_intersection_with_t[0]


def triangle_area(triangle):
    u = triangle[1] - triangle[0]
    v = triangle[2] - triangle[0]
    return 0.5 * np.sqrt(u.dot(u) * v.dot(v) - u.dot(v) ** 2)


def inside_polygon(polygon, point):
    intersections = 0
    for i in range(len(polygon)):
        a = np.array(polygon[i - 1])
        b = np.array(polygon[i])
        u = b - a

        (intersection, t) = line_line_intersection_with_t(
            {"point": a, "vector": u}, {"point": point, "vector": np.array((1, 0))}
        )
        # not ideal, TODO:
        (intersection, s) = line_line_intersection_with_t(
            {"point": point, "vector": np.array((1, 0))}, {"point": a, "vector": u}
        )
        intersections += t is not None and 0 <= t <= 1 and 0 <= s

    return intersections % 2 == 1

