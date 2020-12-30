#!/usr/bin/env python3
import sys
sys.path.insert(0, "../quickdraw/")

import numpy as np
from PIL import Image, ImageDraw
from marching_squares import marching_squares
import quickdraw
import pickle

w, h = 600, 600
img = Image.new("RGBA", (w, h), "#FFFFFFFF")
draw = ImageDraw.Draw(img)

overlay = Image.new("RGBA", (w, h), "#00000000")
overlay_draw = ImageDraw.Draw(overlay)

with open("scenegraph-constraints.model", "rb") as f:
    model = pickle.load(f)
    
step = 10
X = [["desk", "ON", (x - 300)/100, (y - 300)/70] for y in range(0, h, step) for x in range(0, w, step)]
y = model.predict(X)

grid = np.reshape(y, (w // step, h // step))
        
obj = {}
obj["drawing"] = quickdraw.get_quickdraw_drawing("table", 1)
obj["bounds"] = quickdraw.get_quickdraw_obj_bounds(obj)
obj["position"] = (300, 300)
obj["scale"] = 100 / quickdraw.get_obj_width(obj)

quickdraw.draw_quickdraw_obj(draw, obj)

marching_squares(overlay_draw, grid, colour_a="#FF000080", colour_b="#00FF0080")
img.paste(overlay, (0, 0), overlay)
img.show()

