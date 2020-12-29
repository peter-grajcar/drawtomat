#!/usr/bin/env python3
import numpy as np
from PIL import Image, ImageDraw

def get_idx(*args):
    idx = 0
    for arg in args:
        idx <<= 1
        idx |= arg > 0 
    return idx
    
def marching_squares(grid, grid_size=10, colour_a="green", colour_b="red"):
    w, h = grid.shape
    img = Image.new("RGB", ((w - 1) * grid_size, (h - 1) * grid_size), "white")
    draw = ImageDraw.Draw(img)

    unit = grid_size
    half = grid_size / 2

    for i in range(w - 1):
        x = i * unit
        for j in range(h - 1):
            y = j * unit

            a = grid[i, j]
            b = grid[i + 1, j]
            c = grid[i + 1, j + 1]
            d = grid[i, j + 1]
        
            idx = get_idx(a, b, c, d)
            if idx == 0:
                draw.rectangle([
                    x, y,
                    x + unit, y + unit
                ], fill=colour_a)
            elif idx == 1:
                draw.polygon([
                    x, y,
                    x + unit, y,
                    x + unit, y + unit,
                    x + half, y + unit,
                    x, y + half
                ], fill=colour_a)
                draw.polygon([
                    x, y + half,
                    x + half, y + unit,
                    x, y + unit
                ], fill=colour_b)
            elif idx == 2:
                draw.polygon([
                    x, y,
                    x + unit, y,
                    x + unit, y + half,
                    x + half, y + unit,
                    x, y + unit
                ], fill=colour_a)
                draw.polygon([
                    x + unit, y + half,
                    x + unit, y + unit,
                    x + half, y + unit
                ], fill=colour_b)
            elif idx == 3:
                draw.rectangle([
                    x, y,
                    x + unit, y + half
                ], fill=colour_a)
                draw.rectangle([
                    x, y + half,
                    x + unit, y + unit
                ], fill=colour_b)
            elif idx == 4:
                draw.polygon([
                    x, y,
                    x + half, y,
                    x + unit, y + half,
                    x + unit, y + unit,
                    x, y + unit
                ], fill=colour_a)
                draw.polygon([
                    x + half, y,
                    x + unit, y,
                    x + unit, y + half
                ], fill=colour_b)
            elif idx == 5:
                draw.polygon([
                    x, y,
                    x + half, y,
                    x, y + half
                ], fill=colour_a)
                draw.polygon([
                    x + half, y,
                    x + unit, y,
                    x + unit, y + half,
                    x + half, y + unit,
                    x, y + unit,
                    x, y + half
                ], fill=colour_b)
                draw.polygon([
                    x + unit, y + half,
                    x + unit, y + unit,
                    x + half, y + unit
                ], fill=colour_a)
            elif idx == 6:
                draw.rectangle([
                    x, y,
                    x + half, y + unit
                ], fill=colour_a)
                draw.rectangle([
                    x + half, y,
                    x + unit, y + unit
                ], fill=colour_b)
            elif idx == 7:
                draw.polygon([
                    x, y,
                    x + half, y,
                    x, y + half,
                ], fill=colour_a)
                draw.polygon([
                    x + half, y,
                    x + unit, y,
                    x + unit, y + unit,
                    x, y + unit,
                    x, y + half
                ], fill=colour_b)
            elif idx == 8:
                draw.polygon([
                    x, y,
                    x + half, y,
                    x, y + half,
                ], fill=colour_b)
                draw.polygon([
                    x + half, y,
                    x + unit, y,
                    x + unit, y + unit,
                    x, y + unit,
                    x, y + half
                ], fill=colour_a)
            elif idx == 9:
                draw.rectangle([
                    x, y,
                    x + half, y + unit
                ], fill=colour_b)
                draw.rectangle([
                    x + half, y,
                    x + unit, y + unit
                ], fill=colour_a)
            elif idx == 10:
                draw.polygon([
                    x + half, y,
                    x + unit, y,
                    x + unit, y + half
                ], fill=colour_a)
                draw.polygon([
                    x + half, y + unit,
                    x, y + unit,
                    x, y + half
                ], fill=colour_a)
                draw.polygon([
                    x, y,
                    x + half, y,
                    x + unit, y + half,
                    x + unit, y + unit,
                    x + half, y + unit,
                    x, y + half
                ], fill=colour_b)
            elif idx == 11:
                draw.polygon([
                    x + half, y,
                    x + unit, y,
                    x + unit, y + half
                ], fill=colour_a)
                draw.polygon([
                    x, y,
                    x + half, y,
                    x + unit, y + half,
                    x + unit, y + unit,
                    x, y + unit
                ], fill=colour_b)
            elif idx == 12:
                draw.rectangle([
                    x, y,
                    x + unit, y + half
                ], fill=colour_b)
                draw.rectangle([
                    x, y + half,
                    x + unit, y + unit
                ], fill=colour_a)
            elif idx == 13:
                draw.polygon([
                    x, y,
                    x + unit, y,
                    x + unit, y + half,
                    x + half, y + unit,
                    x, y + unit
                ], fill=colour_b)
                draw.polygon([
                    x + unit, y + half,
                    x + unit, y + unit,
                    x + half, y + unit
                ], fill=colour_a)
            elif idx == 14:
                draw.polygon([
                    x, y + half,
                    x + half, y + unit,
                    x, y + unit
                ], fill=colour_a)
                draw.polygon([
                    x, y,
                    x + unit, y,
                    x + unit, y + unit,
                    x + half, y + unit,
                    x, y + half
                ], fill=colour_b)
            elif idx == 15:
                draw.rectangle([x, y, x + unit, y + unit], fill=colour_b)
            
    return img

if __name__ == "__main__":
    w = 40
    h = 30
    grid = np.random.uniform(low=-1, high=1, size=(w, h))
    
    img = marching_squares(grid)
    img.show()

