#!/usr/bin/env python3
#
# Algorithm for positioning with geometrical constraints
#
from PIL import Image, ImageDraw
import numpy as np
from drawing import *
from pprint import pprint

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


def split_extended_polygon_v2(polygon, half_plane):
    result = []

    # 1. filter out points which are on a wrong side of the half-plane
    for i in range(len(polygon)):
        a = polygon[i - 1]
        b = polygon[i]

        if is_vector_vertex(b):
            if is_point_vertex(a):
                side_a = get_side_line(half_plane["line"], a["point"])

                (intersection_point, t) = line_line_intersection_with_t(
                    {"point": a["point"], "vector": b["vector"]}, half_plane["line"]
                )
                if t is not None and t >= 0:
                    result.append({"point": intersection_point})
                    # if a is on a wrong side it means that the polygon was not closed
                    # and thus we want to keep the vector
                    if side_a != half_plane["side"]:
                        result.append(b)
                # if there is no intersection point we want to keep the vector
                else:
                    result.append(b)
        else:
            side_b = get_side_line(half_plane["line"], b["point"])

            if is_vector_vertex(a):
                (intersection_point, t) = line_line_intersection_with_t(
                    {"point": b["point"], "vector": a["vector"]}, half_plane["line"]
                )
                if t is not None and t >= 0:
                    # if a is on a wrong side it means that the polygon was not closed
                    # and thus we want to keep the vector
                    if side_b != half_plane["side"]:
                        result.append(a)
                    result.append({"point": intersection_point})
                # if there is no intersection point we want to keep the vector
                else:
                    result.append(a)
            else:  # a is a point vertex
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

        # a is a point, b is a vector
        # check if the original vector forms a ray which stays inside
        # the half-plane
        c = a["point"] + b["vector"]
        side_c = get_side_line(half_plane["line"], c)
        if side_c != half_plane["side"]:
            # we need to choose new vector which is closer to the half-plane
            # boundary line
            dot_prod = b["vector"].dot(half_plane["line"]["vector"])
            if dot_prod > 0:
                result[j] = {"vector": half_plane["line"]["vector"]}
            else:
                result[j] = {"vector": -half_plane["line"]["vector"]}

    return result


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


def triangle_area(triangle):
    u = triangle[1] - triangle[0]
    v = triangle[2] - triangle[0]
    return 0.5 * np.sqrt(u.dot(u) * v.dot(v) - u.dot(v) ** 2)


def random_points_inside_extended_polygon_v2(polygon, size=1):
    # triangulate finite part of the polygon
    points = [vertex["point"] for vertex in polygon if vertex.get("point") is not None]
    triangles = convex_triangulate(points)

    # compute and assign area of each triangle
    triangles_with_areas = [
        {"triangle": triangle, "area": triangle_area(triangle)}
        for triangle in triangles
    ]
    triangles_with_areas.sort(key=lambda twa: twa["area"])

    total_area = sum([twa["area"] for twa in triangles_with_areas])

    # find all rays
    rays = []
    for i in range(len(polygon)):
        a = polygon[i - 1]
        b = polygon[i]
        if is_point_vertex(a) and is_vector_vertex(b):
            rays.append({"point": a["point"], "vector": b["vector"]})
        if is_point_vertex(b) and is_vector_vertex(a):
            rays.append({"point": b["point"], "vector": a["vector"]})

    result = []

    rs = abs(np.random.normal(scale=3.5, size=size))
    print(sum(rs > 1))
    for r in rs:
        if len(triangles) > 0 and (len(rays) == 0 or r < 1):
            # generate point inside the finite part of the polygon
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
        else:
            # generate point inside the infinite part of the polygon
            # TODO: special cases:
            #         - one half-plane
            #         - two parallel half-planes
            ray_a = rays[0]
            ray_b = rays[1]

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


def extended_polygon_v2_demo(draw, overlay):
    poly = [
        {"vector": np.array((3, -1))},
        {"point": np.array((80, 60))},
        {"point": np.array((40, 80))},
        {"point": np.array((50, 110))},
        {"point": np.array((80, 150))},
        {"vector": np.array((4, 1))},
    ]

    poly = [
        {"vector": np.array((3, -1))},
        {"point": np.array((80, 100))},
        {"vector": np.array((-3, 1))},
    ]

    plane_a = {
        "line": {"point": np.array((125, 125)), "vector": np.array((5, 1)),},
        "side": "L",
        "interval": np.array((-10, 50)),
    }

    draw_extended_poly_v2(draw, poly)
    draw_plane(overlay, plane_a)

    split_poly = split_extended_polygon_v2(poly, plane_a)
    pprint(split_poly)
    draw_extended_poly_v2(draw, split_poly, line_colour="red")

    # for point in random_points_inside_extended_polygon_v2(split_poly, size=1000):
    #    draw_point(draw, point, colour="green")

    # triangles = convex_triangulate(
    #    [vertex for vertex in split_poly if vertex.get("point") is not None]
    # )
    # for triangle in triangles:
    #    draw_extended_poly_v2(draw, triangle, line_colour="yellow")


#############################################
################### MAIN ####################
#############################################

if __name__ == "__main__":
    dimensions = (250, 250)

    img = Image.new("RGBA", dimensions, "white")
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", dimensions, (0, 0, 0, 0))
    pixels = overlay.load()

    extended_polygon_v2_demo(draw, overlay)

    img.paste(overlay, (0, 0), overlay)
    img.show()
