#!/usr/bin/env python3
from geometry import *
from PIL import Image, ImageDraw
import numpy as np
import drawing
import colorsys
import ndjson
import quick_draw
import rdp_algorithm


class side_constraint:
    def __init__(self, obj, side, direction=(0, -1)):
        self.obj = obj
        self.side = side
        self.direction = direction

    def __call__(self, x, y):
        line = {"point": self.obj["position"], "vector": np.array(self.direction)}
        return get_side_line(line, np.array((x, y))) == self.side


class inside_constraint:
    def __init__(self, obj):
        self.obj = obj
        strokes = quick_draw.get_quickdraw_strokes(self.obj)
        self.rdp_strokes = [rdp_algorithm.rdp(stroke, 10) for stroke in strokes]

    def __call__(self, x, y):
        for stroke in self.rdp_strokes:
            if inside_polygon(stroke, np.array((x, y))):
                return True
        return False


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(255 * rgb[0]), int(255 * rgb[1]), int(255 * rgb[2])
    )


if __name__ == "__main__":
    with open("../quickdraw-dataset/saved/house.ndjson") as f:
        houses = ndjson.load(f)

    dimensions = np.array((500, 500))
    img = Image.new("RGBA", tuple(dimensions), "white")
    overlay = Image.new("RGBA", tuple(dimensions), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    house = {
        "drawing": houses[1][
            "drawing"
        ],  # [[[100, 200, 200, 100, 100], [200, 200, 100, 100, 200]]],
        "position": np.array((250, 250)),
        "scale": 0.75,
        "bounds": quick_draw.get_quickdraw_obj_bounds(houses[1]),  # (100,200,100,200)
    }

    quick_draw.draw_quickdraw_obj(draw, house, colour="black")

    constraints = [
        side_constraint(house, "L"),
        inside_constraint(house)
        # side_constraint(house, "L", direction=(-1, 0)),
    ]
    num_of_constraints = len(constraints)

    for i in range(1000):
        rand_point = np.random.normal(scale=100, size=2) + dimensions / 2
        # print(rand_point)
        constraints_satisfied = 0

        for constraint in constraints:
            constraints_satisfied += constraint(rand_point[0], rand_point[1])

        colour = colorsys.hsv_to_rgb(constraints_satisfied / num_of_constraints, 1, 1)
        hex_colour = rgb_to_hex(colour)
        if constraints_satisfied > 0:
            drawing.draw_point(draw, rand_point, colour=hex_colour)

    img.show()
