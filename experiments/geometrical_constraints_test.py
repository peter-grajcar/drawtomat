#!/usr/bin/env python3
from PIL import Image, ImageDraw
import geometrical_constraints
import numpy as np
import ndjson

with open("../quickdraw-dataset/saved/cat.ndjson") as f:
    cats = ndjson.load(f)

with open("../quickdraw-dataset/saved/dog.ndjson") as f:
    dogs = ndjson.load(f)


def draw_quickdraw_obj(draw, obj, cx=0, cy=0, scale=1, colour="red"):
    strokes = [
        [(cx + x * scale, cy + y * scale) for (x, y) in zip(stroke[0], stroke[1])]
        for stroke in obj["drawing"]
    ]

    for stroke in strokes:
        draw.line(stroke, fill=colour)


def get_quickdraw_obj_bounds(obj):
    min_x = None
    min_y = None
    max_x = None
    max_y = None
    for stroke in obj["drawing"]:
        m = max(stroke[0])
        if max_x is None or max_x < m:
            max_x = m
        m = min(stroke[0])
        if min_x is None or min_x > m:
            min_x = m

        m = max(stroke[1])
        if max_y is None or max_y < m:
            max_y = m
        m = min(stroke[1])
        if min_y is None or min_y > m:
            min_y = m

    return (min_x, max_x, min_y, max_y)


def draw_bounding_box(draw, obj, cx=0, cy=0, scale=1, colour="blue"):
    min_x, max_x, min_y, max_y = get_quickdraw_obj_bounds(obj)
    draw.rectangle(
        [
            (cx + min_x * scale, cy + min_y * scale),
            (cx + max_x * scale, cy + max_y * scale),
        ],
        outline=colour,
    )


if __name__ == "__main__":
    dimensions = (500, 500)

    img = Image.new("RGBA", dimensions, "white")
    overlay = Image.new("RGBA", dimensions, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw_quickdraw_obj(draw, cats[1], scale=0.5)
    draw_bounding_box(draw, cats[1], scale=0.5)

    draw_quickdraw_obj(draw, dogs[4], scale=0.5, cx=200)
    draw_bounding_box(draw, dogs[4], scale=0.5, cx=200)

    constraints = [
        {
            "line": {"point": np.array((200, 100)), "vector": np.array((0, 1)),},
            "side": "R",
        },
        {
            "line": {"point": np.array((10, 100)), "vector": np.array((1, 0)),},
            "side": "R",
        },
    ]

    for constraint in constraints:
        geometrical_constraints.draw_plane(overlay, plane=constraint)

    img.paste(overlay, (0, 0), overlay)
    img.show()
