#!/usr/bin/env python3
import sys
import numpy as np
import quickdraw
import pickle
from drawtomat.sklearn.word_encoder import WordEncoder
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.path import Path
import matplotlib.patches as patches

with open(sys.argv[1], "rb") as f:
    model = pickle.load(f)

    print(model)

predicate = sys.argv[2]
subject = sys.argv[3]

if subject:
    X = [[subject.lower(), predicate.upper(), x, y] for y in ys for x in xs]
else:
    X = [[predicate.upper(), x, y] for y in ys for x in xs]

y = model.predict(X)

step = 0.05
xs, ys = np.arange(-2.5, 2.5, step), np.arange(-2.5, 2.5, step)
grid = np.reshape(y, (xs.shape[0], ys.shape[0]))

rc("font",**{"family": "serif", "serif": ["Computer Modern"], "size": 20})
rc("text", usetex=True)
fig, ax = plt.subplots()

if subject:
    # Draw the quickdraw drawing
    obj = {}
    obj["drawing"] = quickdraw.get_quickdraw_drawing(subject.lower(), 2)
    obj["bounds"] = quickdraw.get_quickdraw_obj_bounds(obj)
    obj["position"] = (0, 0)
    obj["scale"] = 1 / quickdraw.get_obj_width(obj)

    for stroke in quickdraw.get_quickdraw_strokes(obj):
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

    ax.set_title(predicate + " " + subject)
else:

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

    ax.set_title(predicate)

# Draw the decision boundary
xs, ys = np.meshgrid(xs, -ys)
plt.contourf(xs, ys, grid, levels=[-1, 0, 1], cmap=plt.cm.bwr_r)
plt.show()
# plt.savefig("figure_" + (predicate + "_" + subject).replace(" ", "_") + ".pdf")

