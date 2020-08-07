#!/usr/bin/env python3
from geometry import *
from PIL import Image, ImageDraw
import numpy as np
import drawing
import colorsys
import ndjson
import quick_draw
import rdp_algorithm
import geometry


class side_constraint:
    def __init__(self, obj, direction=(1, 0)):
        self.obj = obj
        self.direction = np.array(direction)
        self.obj_size = np.array(quick_draw.get_obj_size(obj)) * obj["scale"]

    def __call__(self, x, y):
        norm_vec = np.array((self.direction[1], -self.direction[0]))

        # choose dominant component of direction vector
        # and set the offset to half the size of the object
        # in the direction of the dominant component
        offset = self.obj_size[np.argmax(abs(self.direction))] / 2

        line = {
            "point": self.obj["position"] + self.direction * offset,
            "vector": norm_vec,
        }
        return get_side_line(line, np.array((x, y))) == "R"


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


class on_top_constraint:
    def __init__(self, obj, limit=50):
        self.obj = obj
        self.limit = limit

        strokes = quick_draw.get_quickdraw_strokes(self.obj)
        rdp_strokes = [rdp_algorithm.rdp(stroke, 5) for stroke in strokes]

        w, h = quick_draw.get_obj_size(self.obj)
        is_on_top = (
            lambda point: -0.5
            < (point[1] - obj["position"][1]) / (h * obj["scale"])
            < -0.25
        )
        self.top = [
            point for stroke in rdp_strokes for point in stroke if is_on_top(point)
        ]

    def __call__(self, x, y):
        # TODO: case for single point
        for i in range(len(self.top)):
            a = self.top[i - 1]
            b = self.top[i]
            if not a[0] <= x <= b[0]:
                continue
            dist_a = (x - a[0]) ** 2 + (y - a[1]) ** 2
            dist_b = (x - b[0]) ** 2 + (y - b[1]) ** 2
            if np.sqrt(dist_a + dist_b) < self.limit:
                return True
        return False


def place_object(central_obj, obj, constraints, limit=1000):
    obj_size = max(quick_draw.get_obj_size(obj)) * obj["scale"]

    best_point = {"score": None, "point": None}
    num_of_constraints = len(constraints)
    for i in range(limit):
        rand_point = np.random.normal(scale=obj_size, size=2) + central_obj["position"]
        constraints_satisfied = 0

        for constraint in constraints:
            constraints_satisfied += constraint(rand_point[0], rand_point[1])

        percentage = constraints_satisfied / num_of_constraints

        if best_point["score"] is None or best_point["score"] < percentage:
            best_point = {"score": percentage, "point": rand_point}
        if constraints_satisfied == num_of_constraints:
            break
    print(best_point)
    obj["position"] = best_point["point"]


if __name__ == "__main__":
    with open("../quickdraw-dataset/saved/house.ndjson") as f:
        houses = ndjson.load(f)

    with open("../quickdraw-dataset/saved/fence.ndjson") as f:
        fences = ndjson.load(f)

    with open("../quickdraw-dataset/saved/tree.ndjson") as f:
        trees = ndjson.load(f)

    with open("../quickdraw-dataset/saved/bird.ndjson") as f:
        birds = ndjson.load(f)

    dimensions = np.array((500, 500))
    img = Image.new("RGBA", tuple(dimensions), "white")
    overlay = Image.new("RGBA", tuple(dimensions), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    house = {
        "drawing": houses[1][
            "drawing"
        ],  # [[[100, 200, 200, 100, 100], [200, 200, 100, 100, 200]]],
        "position": np.array((250, 250)),
        "scale": 0.5,
        "bounds": quick_draw.get_quickdraw_obj_bounds(houses[1]),  # (100,200,100,200)
    }

    fence = {
        "drawing": fences[2]["drawing"],
        "position": np.array((325, 425)),
        "scale": 0.2,
        "bounds": quick_draw.get_quickdraw_obj_bounds(fences[2]),
    }

    tree = {
        "drawing": trees[2]["drawing"],
        "scale": 0.4,
        "bounds": quick_draw.get_quickdraw_obj_bounds(trees[2]),
    }

    bird = {
        "drawing": birds[3]["drawing"],
        "scale": 0.1,
        "bounds": quick_draw.get_quickdraw_obj_bounds(birds[3]),
    }

    place_object(
        house,
        tree,
        [
            side_constraint(house, direction=(-1, 0)),
            side_constraint(house, direction=(1, 0)),
        ],
    )
    place_object(fence, bird, [on_top_constraint(fence, limit=10),])

    quick_draw.draw_quickdraw_obj(draw, house, colour="black")
    quick_draw.draw_quickdraw_obj(draw, fence, colour="brown")
    quick_draw.draw_quickdraw_obj(draw, tree, colour="green")
    quick_draw.draw_quickdraw_obj(draw, bird, colour="blue")

    ############################################################################
    rgb_to_hex = lambda rgb: "#{:02x}{:02x}{:02x}".format(
        int(255 * rgb[0]), int(255 * rgb[1]), int(255 * rgb[2])
    )

    central_obj = house
    constraints = [
        side_constraint(house, direction=(-1, 0)),
        side_constraint(house, direction=(1, 0)),
    ]
    num_of_constraints = len(constraints)
    for i in range(5000):
        rand_point = np.random.normal(scale=100, size=2) + central_obj["position"]
        constraints_satisfied = 0

        for constraint in constraints:
            constraints_satisfied += constraint(rand_point[0], rand_point[1])

        percentage = constraints_satisfied / num_of_constraints
        colour = colorsys.hsv_to_rgb((4 + 2 * percentage) / 6, 1, 1)
        hex_colour = rgb_to_hex(colour)
        if constraints_satisfied > 0:
            drawing.draw_point(draw, rand_point, colour=hex_colour)
    ############################################################################

    img.show()
