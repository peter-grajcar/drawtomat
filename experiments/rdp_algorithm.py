#!/usr/bin/env python3
#
# Ramer-Dougles-Peucker Algorithm
#
import tkinter
import math
import ndjson

with open("../quickdraw-dataset/saved/cat.ndjson") as f:
    cats = ndjson.load(f)

px, py = 0, 0
strokes = [
    [(px + x * 0.5, py + y * 0.5) for (x, y) in zip(stroke[0], stroke[1])]
    for stroke in cats[1]["drawing"]
]

# points = [
#    (x, 150 + 100 * math.exp(-x / 60) * math.cos(2 * math.pi * x / 60))
#    for x in range(10, 290)
# ]


def perp_dist(p0, p1, p2):
    denom = math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
    num = abs(
        (p2[1] - p1[1]) * p0[0]
        - (p2[0] - p1[0]) * p0[1]
        + p2[0] * p1[1]
        - p2[1] * p1[0]
    )
    return num / denom


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
            d = perp_dist(points[i], points[start], points[end - 1])
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


root = tkinter.Tk()
root.configure(bg="#4f4f4f")
c = tkinter.Canvas(root)

for points in strokes:
    # c.create_line(points, fill="#ff0000")
    c.create_line(rdp(points, 5), fill="#00ff00")

c.pack(fill="both", expand=1)
root.mainloop()
