#!/usr/bin/env python3
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from marching_squares import marching_squares
import quickdraw
import pickle
from drawtomat.sklearn.word_encoder import WordEncoder

w, h = 600, 600
img = Image.new("RGBA", (w, h), "#FFFFFFFF")
draw = ImageDraw.Draw(img)

overlay = Image.new("RGBA", (w, h), "#00000000")
overlay_draw = ImageDraw.Draw(overlay)

with open(sys.argv[1], "rb") as f:
    model = pickle.load(f)

    print(model)

step = 5
X = [[sys.argv[3], sys.argv[2], (x - 300)/100, (y - 300)/100] for x in range(0, w, step) for y in range(0, h, step)]
y = model.predict(X)

grid = np.reshape(y, (w // step, h // step))
        
obj = {}
obj["drawing"] = quickdraw.get_quickdraw_drawing(sys.argv[3], 1)
obj["bounds"] = quickdraw.get_quickdraw_obj_bounds(obj)
obj["position"] = (300, 300)
obj["scale"] = 100 / quickdraw.get_obj_width(obj)

quickdraw.draw_quickdraw_obj(draw, obj)

#draw.rectangle([250, 250, 350, 350], outline="black")
marching_squares(overlay_draw, grid, colour_a="#FF000080", colour_b="#00FF0080")
overlay_draw.text((10, 10), sys.argv[2] + " " + sys.argv[3].upper(), font=ImageFont.truetype("Verdana.ttf",20), fill="black")

img.paste(overlay, (0, 0), overlay)
img.show()

