#!/usr/bin/env python3
import numpy as np
from PIL import Image, ImageDraw

def get_idx(*args):
    idx = 0
    for arg in args:
        idx <<= 1
        idx |= arg > 1
    return idx
    
def lerp(a, b, t):
    if t <= 0:
        return a
    elif t >= 1:
        return b
    x = b - a
    return a + t*x 

def marching_squares(draw, grid, colour_a="green", colour_b="red"):
    w, h = grid.shape

    unit_x = draw.im.size[0] / (w - 1)
    unit_y = draw.im.size[1] / (h - 1)

    for i in range(w - 1):
        x = i * unit_x
        for j in range(h - 1):
            y = j * unit_y

            a = 1 + grid[i, j]
            b = 1 + grid[i + 1, j]
            c = 1 + grid[i + 1, j + 1]
            d = 1 + grid[i, j + 1]
        
            p0 = (x, y)
            p2 = (x + unit_x, y)
            p4 = (x + unit_x, y + unit_y)
            p6 = (x, y + unit_y)
            
            t = (1 - a) / (b - a)
            p1 = (lerp(x, x + unit_x, t), y)
            t = (1 - b) / (c - b)
            p3 = (x + unit_x, lerp(y, y + unit_y, t))
            t = (1 - d) / (c - d)
            p5 = (lerp(x, x + unit_x, t), y + unit_y)
            t = (1 - a) / (d - a)
            p7 = (x, lerp(y, y + unit_y, t))

            idx = get_idx(a, b, c, d)
            if idx == 0:
                draw.rectangle([p0, p4], fill=colour_a)
            elif idx == 1:
                draw.polygon([p0, p2, p4, p5, p7], fill=colour_a)
                draw.polygon([p7, p5, p6], fill=colour_b)
            elif idx == 2:
                draw.polygon([p0, p2, p3, p5, p6], fill=colour_a)
                draw.polygon([p3, p4, p5], fill=colour_b)
            elif idx == 3:
                draw.polygon([p0, p2, p3, p7], fill=colour_a)
                draw.polygon([p7, p3, p4, p6], fill=colour_b)
            elif idx == 4:
                draw.polygon([p0, p1, p3, p4, p6], fill=colour_a)
                draw.polygon([p1, p2, p3], fill=colour_b)
            elif idx == 5:
                draw.polygon([p0, p1, p7], fill=colour_a)
                draw.polygon([p1, p2, p3, p5, p6, p7], fill=colour_b)
                draw.polygon([p3, p4, p5], fill=colour_a)
            elif idx == 6:
                draw.polygon([p0, p1, p5, p6], fill=colour_a)
                draw.polygon([p1, p2, p4, p5], fill=colour_b)
            elif idx == 7:
                draw.polygon([p0, p1, p7], fill=colour_a)
                draw.polygon([p1, p2, p4, p6, p7], fill=colour_b)
            elif idx == 8:
                draw.polygon([p0, p1, p7], fill=colour_b)
                draw.polygon([p1, p2, p4, p6, p7], fill=colour_a)
            elif idx == 9:
                draw.polygon([p0, p1, p5, p6], fill=colour_b)
                draw.polygon([p1, p2, p4, p5], fill=colour_a)
            elif idx == 10:
                draw.polygon([p1, p2, p3], fill=colour_a)
                draw.polygon([p5, p6, p7], fill=colour_a)
                draw.polygon([p0, p1, p3, p4, p5, p7], fill=colour_b)
            elif idx == 11:
                draw.polygon([p1, p2, p3], fill=colour_a)
                draw.polygon([p0, p1, p3, p4, p6], fill=colour_b)
            elif idx == 12:
                draw.polygon([p0, p2, p3, p7], fill=colour_b)
                draw.polygon([p7, p3, p4, p6], fill=colour_a)
            elif idx == 13:
                draw.polygon([p0, p2, p3, p5, p6], fill=colour_b)
                draw.polygon([p3, p4, p5], fill=colour_a)
            elif idx == 14:
                draw.polygon([p7, p5, p6], fill=colour_a)
                draw.polygon([p0, p2, p4, p5, p7], fill=colour_b)
            elif idx == 15:
                draw.rectangle([p0, p4], fill=colour_b)
            
if __name__ == "__main__":
    w = 51
    h = 51

    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)
    
    grid = np.random.uniform(low=-1, high=1, size=(w, h))
    
    img = marching_squares(draw, grid)
    img.show()

