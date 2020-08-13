import colorsys

import numpy as np
from PIL import Image, ImageDraw

from drawtomat.constraints.inside_constraint import InsideConstraint
from drawtomat.model.physical import PhysicalObject
from drawtomat.model.relational.group import Group
from drawtomat.model.relational.object import Object
from drawtomat.model.relational.scene import Scene


def draw_obj(draw, obj, colour="black"):
    strokes = [
        [
            (x + obj.x, y + obj.y) for x, y in zip(stroke[0], stroke[1])
        ] for stroke in obj.strokes
    ]
    for stroke in strokes:
        draw.line(stroke, fill=colour, width=3)


if __name__ == "__main__":

    dimensions = np.array((500, 500))
    img = Image.new("RGBA", tuple(dimensions), "white")
    overlay = Image.new("RGBA", tuple(dimensions), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    scene = Scene()
    group = Group(scene)

    house_rel = Object(scene, "house", group)
    house = PhysicalObject(house_rel)
    house.set_position(250, 250)
    house.set_scale(0.5)

    draw_obj(draw, house)

    """
    place_object(
        house,
        tree,
        [
            side_constraint(house, direction=(-1, 0)),
            side_constraint(house, direction=(1, 0)),
        ],
    )
    place_object(fence, bird, [on_top_constraint(fence, limit=10),])
    """

    ############################################################################
    rgb_to_hex = lambda rgb: "#{:02x}{:02x}{:02x}".format(
        int(255 * rgb[0]), int(255 * rgb[1]), int(255 * rgb[2])
    )

    central_obj = house
    constraints = [
        # SideConstraint(house, direction=(-1, 0)),
        InsideConstraint(house),
        # OnConstraint(house),
    ]
    num_of_constraints = len(constraints)
    for i in range(5000):
        rand_point = np.random.normal(scale=100, size=2) + np.array(central_obj.get_position())
        constraints_satisfied = 0

        for constraint in constraints:
            constraints_satisfied += constraint(rand_point[0], rand_point[1])

        percentage = constraints_satisfied / num_of_constraints
        colour = colorsys.hsv_to_rgb((4 + 2 * percentage) / 6, 1, 1)
        hex_colour = rgb_to_hex(colour)
        if constraints_satisfied > 0:
            draw.ellipse([tuple(rand_point - np.ones(2)), tuple(rand_point + np.ones(2))], fill=hex_colour)
    ############################################################################

    img.show()

