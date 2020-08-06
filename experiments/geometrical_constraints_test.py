#!/usr/bin/env python3
from PIL import Image, ImageDraw
import geometrical_constraints
import numpy as np
import ndjson
from pprint import pprint
from quick_draw import *

with open("../quickdraw-dataset/saved/clock.ndjson") as f:
    clocks = ndjson.load(f)

with open("../quickdraw-dataset/saved/chair.ndjson") as f:
    chairs = ndjson.load(f)

with open("../quickdraw-dataset/saved/cat.ndjson") as f:
    cats = ndjson.load(f)


if __name__ == "__main__":
    dimensions = (500, 500)

    img = Image.new("RGBA", dimensions, "white")
    overlay = Image.new("RGBA", dimensions, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    clock = {
        "drawing": clocks[1]["drawing"],
        "position": (250, 150),
        "scale": 0.15,
        "bounds": get_quickdraw_obj_bounds(clocks[1]),
    }

    chair = {
        "drawing": chairs[1]["drawing"],
        "position": (350, 250),
        "scale": 0.35,
        "bounds": get_quickdraw_obj_bounds(chairs[1]),
    }

    cat = {
        "drawing": cats[4]["drawing"],
        "position": (0, 0),
        "scale": 0.1,
        "bounds": get_quickdraw_obj_bounds(cats[4]),
    }

    poly = [
        {"vector": np.array((-1, 0))},
        {"point": np.array((300, 190))},
        {"vector": np.array((0, 1))},
    ]

    constraints = [
        {
            "line": {"point": np.array((300, 190)), "vector": np.array((-1, 0)),},
            "side": "L",
        },
        {
            "line": {"point": np.array((300, 190)), "vector": np.array((0, 1)),},
            "side": "R",
        },
    ]

    # geometrical_constraints.draw_extended_poly_v2(draw, poly)
    # for point in geometrical_constraints.random_points_inside_extended_polygon_v2(
    #    poly, size=500
    # ):
    #    geometrical_constraints.draw_point(draw, point, colour="cyan")

    draw_quickdraw_obj(draw, clock, colour="red")
    draw_quickdraw_obj(draw, chair, colour="blue")

    # geometrical_constraints.draw_plane(overlay, constraints[0])
    # geometrical_constraints.draw_plane(overlay, constraints[1])

    cat["position"] = geometrical_constraints.random_points_inside_extended_polygon_v2(
        poly
    )
    draw_quickdraw_obj(draw, cat, colour="green")

    # for constraint in constraints:
    #    geometrical_constraints.draw_plane(overlay, plane=constraint)

    img.paste(overlay, (0, 0), overlay)
    img.show()
