#!/usr/bin/env python3
from PIL import Image, ImageDraw
import quickdraw

obj = {}
obj["drawing"] = quickdraw.get_quickdraw_drawing("cat", 3)
obj["bounds"] = quickdraw.get_quickdraw_obj_bounds(obj)
obj["position"] = (200, 200)
obj["scale"] = 100 / quickdraw.get_obj_width(obj)

img = Image.new("RGB", (400, 400), "white")
draw = ImageDraw.Draw(img)

quickdraw.draw_quickdraw_obj(draw, obj)

img.show()

