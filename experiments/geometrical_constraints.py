#!/usr/bin/env python3
#
# Algorithm for positioning with geometrical constraints
#
from PIL import Image, ImageDraw
import numpy as np

epsilon = 1e-8


def line_line_intersection_with_t(line_a, line_b):
    w = line_a["point"] - line_b["point"]
    u = line_a["vector"]
    v = line_b["vector"]
    nv = np.array((-v[1], v[0]))

    angle = nv.dot(u)
    if abs(angle - 0) < epsilon:
        return None

    t = -nv.dot(w) / angle
    return (line_a["point"] + u * t, t)


def line_line_intersection(line_a, line_b):
    return line_line_intersection_with_t[0]


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


def draw_point(draw, point, color="magenta"):
    draw.ellipse([tuple(point - 1), tuple(point + 1)], fill=color)


def draw_line(draw, line, color="blue"):
    A = line["point"]
    u = line["vector"]
    dim = np.argmax(u)
    t_a = -A[dim] / u[dim]
    t_b = (dimensions[dim] - A[dim]) / u[dim]
    draw_point(draw, A)
    draw.line([tuple(A + t_a * u), tuple(A + t_b * u)], fill=color)


def draw_segment(draw, start, end, color="blue"):
    draw.line([tuple(start), tuple(end)], fill=color)


def draw_poly(draw, points, segment_color="blue", point_color="magenta"):
    for i in range(0, len(points)):
        a = points[i - 1]
        b = points[i]

        a_clipped, b_clipped = clip_line(a, b, draw.im.size[0], draw.im.size[1])

        draw_point(draw, b_clipped, color=point_color)
        draw_segment(draw, a_clipped, b_clipped, color=segment_color)


def intersection_test():
    lines = [line_a, line_b, line_c]
    for line in lines:
        draw_line(line)

    intersections = np.array(
        [line_line_intersection(a, b) for a in lines for b in lines if a is not b]
    )

    for intersection in intersections:
        draw.ellipse(
            [
                (intersection[0] - 2, intersection[1] - 2),
                (intersection[0] + 2, intersection[1] + 2),
            ],
            fill="red",
        )

    centre = np.mean(intersections, axis=0)
    draw.ellipse(
        [(centre[0] - 2, centre[1] - 2), (centre[0] + 2, centre[1] + 2),], fill="green",
    )


def draw_plane(overlay, plane):
    A = plane["line"]["point"]
    u = plane["line"]["vector"]
    sign = 1 if plane["side"] == "R" else -1
    # I = plane["interval"]

    u = u / np.max(u)
    n = np.array((-u[1], u[0])) * sign

    size = np.array((2, 2))
    # draw.ellipse([tuple(A - size), tuple(A + size)], fill="green")

    # find bounds [t_a, t_b] of parameter t in the parametric equation P = A + u * t
    # such that they are in the interval I
    dim = np.argmax(u)
    t_a = -A[dim] / u[dim]  # max(I[0], -A[dim] / u[dim])
    t_b = (overlay.size[dim] - A[dim]) / u[
        dim
    ]  # min(I[1], (dimensions[dim] - A[dim]) / u[dim])

    # draw.line([tuple(A + t_a * u), tuple(A + t_b * u)], fill="blue")
    # draw.line([tuple(A), tuple(A + u * 20)], fill="red")

    pixels = overlay.load()
    for i in range(0, overlay.size[0], 2):
        for j in range(0, overlay.size[1], 2):
            p = np.array((i, j))

            # projection onto a line (u*u^T)/(u^T*u) * p
            proj = (np.outer(u, u) / np.dot(u, u)) @ p

            # fill point if it is on the right side and its projection is within interval bounds
            if plane["side"] == get_side_line(
                plane["line"], p
            ):  # and proj[dim] > t_a and proj[dim] < t_b:
                old_pixel = pixels[i, j]
                pixels[i, j] = (
                    64,
                    255 - old_pixel[1] - 32,
                    255 - old_pixel[2] - 32,
                    32,
                )


def split_polygon(polygon, half_plane):
    result = []

    side_a = get_side_line(half_plane["line"], polygon[-1])
    for i in range(0, len(polygon)):
        a = polygon[i - 1]
        b = polygon[i]
        side_b = get_side_line(half_plane["line"], b)

        if side_a != side_b:
            ab_line = {"point": a, "vector": b - a}
            (intersect_point, t) = line_line_intersection_with_t(
                ab_line, half_plane["line"]
            )
            draw_point(draw, intersect_point, "#906090")

            # add intersection point
            result.append(intersect_point)

        if side_b == half_plane["side"]:
            result.append(b)

        side_a = side_b

    return result


# returns True if point lies inside triangle abc
def inside_triangle(a, b, c, point):
    s1 = get_side(a, b, point)
    s2 = get_side(b, c, point)
    s3 = get_side(c, a, point)
    return s1 == s2 and s2 == s3


def convex_triangulate(poly):
    polygon = [vertex for vertex in poly]
    triangles = []
    n = len(polygon)

    while n > 3:
        m = n >> 1
        for i in range(m):
            a = polygon[i]
            b = polygon[i + 1]
            c = polygon[(i + 2) % n]
            triangles.append((a, b, c))
            del polygon[i + 1]
            n -= 1

    if n == 3:
        triangles.append(polygon)

    return triangles


def triangulate(polygon):
    triangles = []
    n = len(polygon)

    i = 0
    while n > 3:
        a = polygon[i - 1]
        b = polygon[i]
        c = polygon[(i + 1) % n]

        # b is a convex vertex
        if get_side(a, c, b) == "L":
            i = (i + 1) % n
            continue

        is_ear = True
        for j in range(n):
            if abs(j - i) > 1 and inside_triangle(a, b, c, polygon[j]):
                is_ear = False
                break

        if is_ear:
            triangles.append((a, b, c))
            del polygon[i]
            n -= 1
        else:
            i = (i + 1) % n

    a, b, c = polygon[0], polygon[1], polygon[2]
    triangles.append((a, b, c))

    return triangles


def is_inf_point(point):
    for coord in point:
        if abs(coord) == np.inf:
            return True
    return False


def clip_line(a, b, width, height):
    if is_inf_point(a) and is_inf_point(b):
        a = np.array((np.clip(a[0], 0, width), np.clip(a[1], 0, height)))
        b = np.array((np.clip(b[0], 0, width), np.clip(b[1], 0, height)))
    elif is_inf_point(a):
        if abs(a[0]) == np.inf and abs(a[1]) == np.inf:
            v = np.array((np.sign(a[0]), np.sign(a[1])))
            t1 = (width - b[0]) if a[0] > 0 else (b[0])
            t2 = (height - b[1]) if a[1] > 0 else (b[1])
            t = min(t1, t2)
            a = b + t * v
        elif abs(a[0]) == np.inf:
            a = np.array((np.clip(a[0], 0, width), b[1]))
        elif abs(a[1]) == np.inf:
            a = np.array((b[0], np.clip(a[1], 0, height)))
    elif is_inf_point(b):
        b, a = clip_line(b, a, width, height)  # prasarna
    return a, b


def triangle_area(triangle):
    u = triangle[1] - triangle[0]
    v = triangle[2] - triangle[0]
    return 0.5 * np.sqrt(u.dot(u) * v.dot(v) - u.dot(v) ** 2)


def random_points_inside_convex_polygon(polygon, size=1):
    triangles = convex_triangulate(polygon)

    triangles_with_areas = [
        {"triangle": triangle, "area": triangle_area(triangle)}
        for triangle in triangles
    ]
    triangles_with_areas.sort(key=lambda twa: twa["area"])
    total_area = sum([twa["area"] for twa in triangles_with_areas])

    print(abs(np.random.normal(size=10)))

    rs = np.random.uniform(size=size)
    points = []
    for r in rs:
        a = 0
        for twa in triangles_with_areas:
            a += twa["area"] / total_area
            if a > r:
                break

        u = twa["triangle"][1] - twa["triangle"][0]
        v = twa["triangle"][2] - twa["triangle"][0]
        alpha, beta = np.random.uniform(size=2)
        if alpha + beta > 1:
            alpha = 1 - alpha
            beta = 1 - beta

        points.append(twa["triangle"][0] + (alpha * u + beta * v))

    return points


if __name__ == "__main__":
    dimensions = (250, 250)

    img = Image.new("RGBA", dimensions, "white")
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", dimensions, (0, 0, 0, 0))
    pixels = overlay.load()

    # half-planes
    plane_a = {
        "line": {"point": np.array((90, 100)), "vector": np.array((4, 24)),},
        "side": "L",
        "interval": np.array((-10, 50)),
    }

    plane_b = {
        "line": {"point": np.array((140, 150)), "vector": np.array((-6, -2)),},
        "side": "R",
        "interval": np.array((-30, 30)),
    }

    plane_c = {
        "line": {"point": np.array((140, 100)), "vector": np.array((-6, -2)),},
        "side": "L",
        "interval": np.array((-30, 30)),
    }

    line_a = {"point": np.array((50, 135)), "vector": np.array((10, -15))}

    line_b = {"point": np.array((70, 55)), "vector": np.array((5, 5))}

    line_c = {"point": np.array((200, 80)), "vector": np.array((-10, 5))}

    polygon = [
        np.array((60, 80)),
        np.array((100, 60)),
        np.array((140, 80)),
        np.array((160, 120)),
        np.array((140, 140)),
        np.array((80, 180)),
        np.array((30, 150)),
    ]
    # draw_plane(plane_a)
    # draw_plane(plane_b)
    # draw_plane(plane_c)

    # draw_plane(plane_a)
    # draw_plane(plane_b)

    """
    draw_line(draw, plane_a["line"], color="magenta")
    draw_line(draw, plane_b["line"], color="magenta")
    draw_line(draw, plane_c["line"], color="magenta")
    draw_poly(draw, polygon, point_color="green", segment_color="green")

    poly_a = split_polygon(polygon, plane_a)
    poly_b = split_polygon(poly_a, plane_b)
    poly_c = split_polygon(poly_b, plane_c)
    draw_poly(draw, poly_c, segment_color="red", point_color="red")
    """

    """
    for poly in convex_triangulate(poly_b):
        print(poly)
        draw_poly(poly, segment_color="red", point_color="red")
    """

    """
    for point in polygon:
        side = get_side(plane_b["line"], point)
        if side == plane_b["side"]:
            draw_point(point, color="red
    """

    poly = [
        np.array((110, 50)),
        np.array((80, 100)),
        np.array((90, 150)),
        np.array((120, 180)),
        np.array((180, 200)),
        np.array((190, 40)),
    ]

    poly_inf = [
        np.array((np.inf, np.inf)),
        np.array((np.inf, -np.inf)),
        np.array((-np.inf, -np.inf)),
        np.array((-np.inf, np.inf)),
    ]

    for triangle in convex_triangulate(poly_inf):
        draw_poly(draw, triangle)

    for point in random_points_inside_convex_polygon(poly, size=500):
        draw_point(draw, point, color="green")

    for triangle in convex_triangulate(poly):
        draw_poly(draw, triangle)

    img.paste(overlay, (0, 0), overlay)
    img.show()
