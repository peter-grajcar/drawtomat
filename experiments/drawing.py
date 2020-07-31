from PIL import Image, ImageDraw
import numpy as np


def get_side_line(line, point):
    u = line["vector"]
    v = point - line["point"]
    nv = np.array((-v[1], v[0]))
    angle = u.dot(nv)
    return "R" if angle < 0 else "L"


def draw_point(draw, point, colour="magenta"):
    draw.ellipse([tuple(point - 1), tuple(point + 1)], fill=colour)


def draw_line(draw, line, colour="blue"):
    A = line["point"]
    u = line["vector"]
    dim = np.argmax(u)
    t_a = -A[dim] / u[dim]
    t_b = (draw.im.size[dim] - A[dim]) / u[dim]
    draw_point(draw, A)
    draw.line([tuple(A + t_a * u), tuple(A + t_b * u)], fill=colour)


def draw_segment(draw, start, end, colour="blue"):
    draw.line([tuple(start), tuple(end)], fill=colour)


def draw_poly(draw, points, segment_colour="blue", point_colour="magenta"):
    for i in range(0, len(points)):
        a = points[i - 1]
        b = points[i]

        # a_clipped, b_clipped = clip_line(a, b, draw.im.size[0], draw.im.size[1])

        draw_point(draw, b, colour=point_colour)
        draw_segment(draw, a, b, colour=segment_colour)


def draw_extended_poly(draw, polygon, line_colour="blue", point_colour="magenta"):
    for i in range(0, len(polygon)):
        a = polygon[i - 1]["point"]
        b = polygon[i]["point"]

        draw_point(draw, b, colour=point_colour)

        if (
            polygon[i - 1].get("vector") is not None
            and polygon[i].get("vector") is not None
        ):
            draw_ray(draw, polygon[i - 1], colour=line_colour)
            draw_ray(draw, polygon[i], colour=line_colour)
        else:
            draw_segment(draw, a, b, colour=line_colour)


def is_point_vertex(vertex):
    return vertex.get("point") is not None


def is_vector_vertex(vertex):
    return vertex.get("vector") is not None


def draw_extended_poly_v2(draw, polygon, line_colour="blue", point_colour="magenta"):
    for i in range(0, len(polygon)):
        a = polygon[i - 1]
        b = polygon[i]

        if is_point_vertex(b):
            draw_point(draw, b["point"], colour=point_colour)

        if is_point_vertex(a) and is_vector_vertex(b):
            draw_ray(
                draw, {"point": a["point"], "vector": b["vector"]}, colour=line_colour
            )
        elif is_point_vertex(b) and is_vector_vertex(a):
            draw_ray(
                draw, {"point": b["point"], "vector": a["vector"]}, colour=line_colour
            )
        elif is_point_vertex(a) and is_point_vertex(b):
            draw_segment(draw, a["point"], b["point"], colour=line_colour)


def draw_ray(draw, ray, colour="blue"):
    A = ray["point"]
    u = ray["vector"]
    dim = np.argmax(u)
    t = max(-A[dim] / u[dim], (draw.im.size[dim] - A[dim]) / u[dim])
    draw.line([tuple(A), tuple(A + t * u)], fill=colour)


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

