#!/usr/bin/env python3
import sys
import numpy as np
import pickle
from drawtomat.sklearn.word_encoder import WordEncoder
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.path import Path
import matplotlib.patches as patches
from drawtomat.constraints import DisjunctionConstraint, SideConstraint, OnConstraint, InsideConstraint, ClassifierConstraint
from drawtomat.composer.factory.quickdraw_object_factory import QuickDrawObjectFactory
from drawtomat.constraints import DisjunctionConstraint, SideConstraint
from drawtomat.model.scenegraph.object import Object
from drawtomat.model.scenegraph.scene import Scene
from drawtomat.model.scenegraph.group import Group
import random

random.seed(42)

scene = Scene()
group = Group(scene)
factory = QuickDrawObjectFactory()
obj_rel = Object(scene, "house", group)
obj = factory.get_physical_object(obj_rel, default_size=1)
"""obj.strokes = [
    [
        [-.5,  .5, .5, -.5, -.5],
        [-.5, -.5, .5,  .5, -.5],
        [0, 1, 2, 3, 4]
    ]
]"""
obj.set_position(0, 0)
obj.set_scale(1)



pred = "in house"

"""
constraint = DisjunctionConstraint(obj, pred, [
    SideConstraint(obj, pred, direction=(-1, 0), offset=.075),
    SideConstraint(obj, pred, direction=(1, 0), offset=.075),
])
"""
constraint = InsideConstraint(obj, pred)
# constraint = OnConstraint(obj, pred, limit=0.25)
#constraint = SideConstraint(obj, pred, direction=(0, 1), offset=.075)
#constraint = ClassifierConstraint(obj, "IN")

step = 0.05
grid_xs, grid_ys = np.arange(-2.5, 2.5, step), np.arange(-2.5, 2.5, step)

xs = np.array([x for y in grid_ys for x in grid_xs])
ys = np.array([y for y in grid_ys for x in grid_xs])
grid = np.reshape(constraint(xs, ys), [grid_ys.shape[0], grid_xs.shape[0]])

rc("font",**{"family": "serif", "serif": ["Computer Modern"], "size": 20})
rc("text", usetex=True)
fig, ax = plt.subplots()
ax.set_title(pred)

strokes = [
    [
        (x + obj.x, y + obj.y) for x, y in zip(stroke[0], stroke[1])
    ] for stroke in obj.strokes
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


# draw decision boundary
grid_xs, grid_ys = np.meshgrid(grid_xs, -grid_ys)
plt.contourf(grid_xs, grid_ys, grid, levels=[-1, 0, 1], cmap=plt.cm.bwr_r)

# draw box
"""
verts = []
codes = []
for (x, y) in [(-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5), (-.5, -.5)]:
    verts.append((x, -y))
    if not codes:
        codes.append(Path.MOVETO)
    else:
        codes.append(Path.LINETO)

path = Path(verts, codes)
patch = patches.PathPatch(path, facecolor='none', lw=0.25, joinstyle="round")
ax.add_patch(patch)
"""
#plt.xlim(-1.5, 1.5)
#plt.ylim(-1.5, 1.5)

plt.show()

