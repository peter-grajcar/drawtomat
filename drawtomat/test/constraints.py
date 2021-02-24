import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from matplotlib.path import Path

from drawtomat.constraints import InsideConstraint
from drawtomat.model.scenegraph.group import Group
from drawtomat.model.scenegraph.object import Object
from drawtomat.model.scenegraph.scene import Scene
from drawtomat.quickdraw.quickdraw_object_factory import QuickDrawObjectFactory

if __name__ == "__main__":

    scene = Scene()
    group = Group(scene)

    factory = QuickDrawObjectFactory()

    house_rel = Object(scene, "house", group)
    house = factory.get_physical_object(house_rel, default_size=1)
    house.set_position(0, 0)
    house.set_scale(1)

    couch_rel = Object(scene, "couch", group)
    couch = factory.get_physical_object(couch_rel)
    couch.set_position(200, 300)
    couch.set_scale(1)

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
        # DisjunctionConstraint(house, "NEXT TO", [
        #    SideConstraint(house, "NEXT TO", direction=(-1, 0)),
        #    SideConstraint(house, "NEXT TO", direction=(1, 0)),
        # ])
        InsideConstraint(house, "INSIDE"),
        # OnConstraint(couch, "ON"),
        # BoxConstraint(house, "IN FRONT OF", scale=1.5),
    ]

    num_of_constraints = len(constraints)
    constraints_satisfied = np.zeros(shape=(1000,))

    centre = central_obj.get_position()
    xs = np.random.normal(scale=1, size=1000)
    ys = np.random.normal(scale=1, size=1000)

    for constraint in constraints:
        constraint.init()
        constraints_satisfied += constraint(xs, ys)

    rc("text", usetex=True)
    fig, ax = plt.subplots()

    strokes = [
        [
            (x + house.x, y + house.y) for x, y in zip(stroke[0], stroke[1])
        ] for stroke in house.strokes
    ]

    for stroke in strokes:
        verts = []
        codes = []
        for (x, y) in stroke:
            verts.append((x, -y))
            if not codes:
                codes.append(Path.MOVETO)
            else:
                codes.append(Path.LINETO)

        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor='none', lw=0.25, joinstyle="round")
        ax.add_patch(patch)

    plt.xlim(-2.5, 2.5)
    plt.ylim(-2.5, 2.5)
    plt.scatter([x for i, x in enumerate(xs) if constraints_satisfied[i] > 0],
                [-y for i, y in enumerate(ys) if constraints_satisfied[i] > 0],
                marker="+")
    ############################################################################

    plt.show()
