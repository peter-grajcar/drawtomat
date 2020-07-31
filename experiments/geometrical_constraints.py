#!/usr/bin/env python3
#
# Algorithm for positioning with geometrical constraints
#
from PIL import Image, ImageDraw
import numpy as np
from drawing import *

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

            # add intersection point
            result.append(intersect_point)

        if side_b == half_plane["side"]:
            result.append(b)

        side_a = side_b

    return result


def split_extended_polygon(polygon, half_plane):
    result = []

    for i in range(0, len(polygon)):
        a = polygon[i - 1]["point"]
        b = polygon[i]["point"]

        side_a = get_side_line(half_plane["line"], a)
        side_b = get_side_line(half_plane["line"], b)

        # b is a closed vertex
        if polygon[i].get("vector") is None:
            if side_a != side_b:
                ab_line = {"point": a, "vector": b - a}
                (intersect_point, t) = line_line_intersection_with_t(
                    ab_line, half_plane["line"]
                )
                result.append({"point": intersect_point})
            if side_b == half_plane["side"]:
                result.append({"point": b})
        # b is an open vertex
        else:
            if side_b == half_plane["side"]:
                ab_line = {"point": a, "vector": b - a}
                (intersect_point, t) = line_line_intersection_with_t(
                    ab_line, half_plane["line"]
                )

                # add intersection point, but only if a is a closed point
                if polygon[i - 1].get("vector") is None:
                    result.append({"point": intersect_point})
                result.append(polygon[i])

            else:
                (intersect_point, t) = line_line_intersection_with_t(
                    polygon[i], half_plane["line"]
                )

                result.append(
                    {"point": intersect_point, "vector": polygon[i]["vector"]}
                )

    return result


def split_extended_polygon_v2(polygon, half_plane):
    result = []
    # 1. filter out points which are on a wrong side of the half-plane
    for i in range(len(polygon)):
        a = polygon[i - 1]
        b = polygon[i]

        if is_vector_vertex(b):
            if is_point_vertex(a):
                (intersection_point, t) = line_line_intersection_with_t(
                    {"point": a["point"], "vector": b["vector"]}, half_plane["line"]
                )

                if t is not None and t >= 0:
                    result.append({"point": intersection_point})

            result.append(b)
        else:
            side_b = get_side_line(half_plane["line"], b["point"])

            if is_vector_vertex(a):
                (intersection_point, t) = line_line_intersection_with_t(
                    {"point": b["point"], "vector": a["vector"]}, half_plane["line"]
                )

                if t is not None and t >= 0:
                    result.append({"point": intersection_point})
            elif is_point_vertex(a):
                side_a = get_side_line(half_plane["line"], a["point"])

                if side_a != side_b:
                    ab_line = {"point": a["point"], "vector": b["point"] - a["point"]}
                    (intersection_point, t) = line_line_intersection_with_t(
                        ab_line, half_plane["line"]
                    )
                    result.append({"point": intersection_point})

            if side_b == half_plane["side"]:
                result.append(b)

    # 2. filter out vectors which have a wrong direction
    for i in range(len(result)):
        a = result[i - 1]
        b = result[i]

        j = i
        if is_point_vertex(a) and is_vector_vertex(b):
            pass
        elif is_point_vertex(b) and is_vector_vertex(a):
            a, b = b, a
            j = i - 1
        else:
            continue

        # a - point, b - vector
        c = a["point"] + b["vector"]
        side_c = get_side_line(half_plane["line"], c)
        if side_c != half_plane["side"]:
            dot_prod = b["vector"].dot(half_plane["line"]["vector"])
            if dot_prod > 0:
                result[j] = {"vector": half_plane["line"]["vector"]}
            else:
                result[j] = {"vector": -half_plane["line"]["vector"]}

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


def random_points_inside_extended_polygon(polygon, size=1):
    points = [vertex["point"] for vertex in polygon]
    triangles = convex_triangulate(points)
    triangles_with_areas = [
        {"triangle": triangle, "area": triangle_area(triangle)}
        for triangle in triangles
    ]
    triangles_with_areas.sort(key=lambda twa: twa["area"])
    total_area = sum([twa["area"] for twa in triangles_with_areas])

    extended_points = [vertex for vertex in polygon if vertex.get("vector") is not None]

    result = []

    rs = (
        np.random.uniform(size=size)
        if len(extended_points) == 0
        else np.random.normal(scale=10, size=size)
    )
    for r in rs:
        # generate random point inside finite part of the polygon
        if len(triangles) > 0 and (r < 1 or len(extended_points) == 0):
            r = np.random.uniform()
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

            result.append(twa["triangle"][0] + (alpha * u + beta * v))
        # generate random point outside of the finite part of the polygon
        else:
            ray_a = extended_points[0]
            ray_b = extended_points[1]

            unit_a = ray_a["vector"] / np.linalg.norm(ray_a["vector"])
            unit_b = ray_b["vector"] / np.linalg.norm(ray_b["vector"])

            t = abs(np.random.normal(scale=50))
            s = np.random.uniform()
            a = ray_a["point"] + t * unit_a
            b = ray_b["point"] + t * unit_b
            v = b - a
            point = a + s * v
            result.append(point)

    return result


##############################################
################### DEMOS ####################
##############################################


def polygon_splitting_demo(draw):
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

    polygon = [
        np.array((60, 80)),
        np.array((100, 60)),
        np.array((140, 80)),
        np.array((160, 120)),
        np.array((140, 140)),
        np.array((80, 180)),
        np.array((30, 150)),
    ]

    draw_line(draw, plane_a["line"], colour="magenta")
    draw_line(draw, plane_b["line"], colour="magenta")
    draw_line(draw, plane_c["line"], colour="magenta")
    draw_poly(draw, polygon, point_colour="green", segment_colour="green")

    poly_a = split_polygon(polygon, plane_a)
    poly_b = split_polygon(poly_a, plane_b)
    poly_c = split_polygon(poly_b, plane_c)
    draw_poly(draw, poly_c, segment_colour="red", point_colour="red")


def convex_triangulation_demo(draw):
    poly = [
        np.array((110, 50)),
        np.array((80, 100)),
        np.array((90, 150)),
        np.array((120, 180)),
        np.array((180, 200)),
        np.array((190, 40)),
    ]

    for point in random_points_inside_convex_polygon(poly, size=500):
        draw_point(draw, point, colour="green")

    for triangle in convex_triangulate(poly):
        draw_poly(draw, triangle)


def random_points_demo(draw):
    ##################################################
    # Generates random points inside area bounded by #
    # two rays                                       #
    ##################################################
    line_a = {"point": np.array((40, 80)), "vector": np.array((2, -1))}
    line_b = {"point": np.array((60, 160)), "vector": np.array((3, 1))}
    draw_line(draw, line_a)
    draw_line(draw, line_b)

    unit_a = line_a["vector"] / np.linalg.norm(line_a["vector"])
    unit_b = line_b["vector"] / np.linalg.norm(line_b["vector"])

    ts = abs(np.random.normal(scale=80, size=500))
    ss = np.random.uniform(size=500)
    for t, s in zip(ts, ss):
        a = line_a["point"] + t * unit_a
        b = line_b["point"] + t * unit_b
        v = b - a
        point = a + s * v
        draw_point(draw, point)

    ##################################################
    # Generates random points inside area bounded by #
    # one half-plane                                 #
    ##################################################
    perp_a = np.array((-unit_a[1], unit_a[0]))
    ts = np.random.normal(scale=80, size=500)
    ss = abs(np.random.normal(scale=80, size=500))
    for t, s in zip(ts, ss):
        x = line_a["point"] + t * unit_a
        point = x + s * perp_a
        draw_point(draw, point, colour="yellow")


def extended_polygon_random_points_demo(draw):
    poly = [
        {"point": np.array((80, 60)), "vector": np.array((3, -1))},
        {"point": np.array((40, 80))},
        {"point": np.array((50, 110))},
        {"point": np.array((80, 150)), "vector": np.array((4, 1))},
    ]

    draw_extended_poly(draw, poly)
    for triangle in convex_triangulate([vertex["point"] for vertex in poly]):
        draw_poly(draw, triangle, segment_colour="green")

    for point in random_points_inside_extended_polygon(poly, size=1000):
        draw_point(draw, point, colour="red")


def extended_polygon_splitting_demo(draw, overlay):
    plane_a = {
        "line": {"point": np.array((60, 100)), "vector": np.array((1, 0)),},
        "side": "L",
        "interval": np.array((-10, 50)),
    }

    poly = [
        {"point": np.array((80, 60)), "vector": np.array((3, -1))},
        {"point": np.array((40, 80))},
        {"point": np.array((50, 110))},
        {"point": np.array((80, 150)), "vector": np.array((4, 1))},
    ]

    draw_extended_poly(draw, poly, line_colour="yellow")

    draw_plane(overlay, plane_a)
    draw_extended_poly(
        draw,
        split_extended_polygon(poly, plane_a),
        line_colour="red",
        point_colour="red",
    )


def extended_polygon_v2_test(draw, overlay):
    poly = [
        {"vector": np.array((3, -1))},
        {"point": np.array((80, 60))},
        {"point": np.array((40, 80))},
        {"point": np.array((50, 110))},
        {"point": np.array((80, 150))},
        {"vector": np.array((4, 1))},
    ]

    plane_a = {
        "line": {"point": np.array((125, 125)), "vector": np.array((5, 10)),},
        "side": "L",
        "interval": np.array((-10, 50)),
    }

    draw_extended_poly_v2(draw, poly)
    draw_plane(overlay, plane_a)

    split_poly = split_extended_polygon_v2(poly, plane_a)
    draw_extended_poly_v2(draw, split_poly, line_colour="red")


#############################################
################### MAIN ####################
#############################################

if __name__ == "__main__":
    dimensions = (250, 250)

    img = Image.new("RGBA", dimensions, "white")
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", dimensions, (0, 0, 0, 0))
    pixels = overlay.load()

    # polygon_splitting_demo(draw)
    # convex_triangulation_demo(draw)
    # random_points_demo(draw)
    # extended_polygon_random_points_demo(draw)
    # extended_polygon_splitting_demo(draw, overlay)
    extended_polygon_v2_test(draw, overlay)

    img.paste(overlay, (0, 0), overlay)
    img.show()
