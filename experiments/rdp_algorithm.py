#!/usr/bin/env python3
#
# Ramer-Dougles-Peucker Algorithm
#
import tkinter
import math
import ndjson
import geometry


def rdp(points: "list", epsilon: "float"):
    stack = [(0, len(points))]
    result_stack = []

    while stack:
        op = stack.pop()
        if op == "merge":
            r1 = result_stack.pop()
            r2 = result_stack.pop()
            result_stack.append(r1 + r2)
            continue
        start, end = op

        dmax = 0
        index = 0
        for i in range(start + 1, end - 2):
            d = geometry.perp_dist(points[i], points[start], points[end - 1])
            if d > dmax:
                dmax = d
                index = i

        if dmax > epsilon:
            stack.append("merge")
            stack.append((start, index))
            stack.append((index, end))
        else:
            result_stack.append([points[start], points[end - 1]])

    return result_stack[0]


if __name__ == "__main__":
    root = tkinter.Tk()
    root.configure(bg="#4f4f4f")
    c = tkinter.Canvas(root)

    with open("../quickdraw-dataset/saved/fence.ndjson") as f:
        fences = ndjson.load(f)

    px, py = 0, 0
    strokes = [
        [(px + x * 0.5, py + y * 0.5) for (x, y) in zip(stroke[0], stroke[1])]
        for stroke in fences[2]["drawing"]
    ]

    for points in strokes:
        c.create_line(points, fill="#00ff00", width=2)
        c.create_line(rdp(points, 10), fill="#ff0000", width=2)

    c.pack(fill="both", expand=1)
    root.mainloop()
