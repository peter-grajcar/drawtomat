import ndjson
from PIL import ImageDraw


def get_quickdraw_drawing(word, idx=0):
    with open(f"../../quickdraw-dataset/saved/{word}.ndjson") as f:
        return ndjson.loads(f.read())[idx]["drawing"]

def get_obj_width(obj):
    return obj["bounds"][1] - obj["bounds"][0]

def get_obj_height(obj):
    return obj["bounds"][3] - obj["bounds"][2]

def get_obj_size(obj):
    return get_obj_width(obj), get_obj_height(obj)

def get_quickdraw_strokes(obj):
    w, h = get_obj_size(obj)
    off_x, off_y = obj["bounds"][0] + w / 2, obj["bounds"][2] + h / 2
    return [
        [
            (
                obj["position"][0] + (x - off_x) * obj["scale"],
                obj["position"][1] + (y - off_y) * obj["scale"],
            )
            for (x, y) in zip(stroke[0], stroke[1])
        ]
        for stroke in obj["drawing"]
    ]


def draw_quickdraw_obj(draw, obj, colour="black", bounding_box=False):
    strokes = get_quickdraw_strokes(obj)
    w, h = get_obj_size(obj)

    if bounding_box:
        draw.rectangle(
            [
                (
                    obj["position"][0] - (w / 2) * obj["scale"],
                    obj["position"][1] - (h / 2) * obj["scale"],
                ),
                (
                    obj["position"][0] + (w / 2) * obj["scale"],
                    obj["position"][1] + (h / 2) * obj["scale"],
                ),
            ],
            outline=colour,
        )

    for stroke in strokes:
        draw.line(stroke, fill=colour, width=1)

def get_quickdraw_obj_bounds(obj):
    min_x = None
    min_y = None
    max_x = None
    max_y = None
    for stroke in obj["drawing"]:
        m = max(stroke[0])
        if max_x is None or max_x < m:
            max_x = m
        m = min(stroke[0])
        if min_x is None or min_x > m:
            min_x = m

        m = max(stroke[1])
        if max_y is None or max_y < m:
            max_y = m
        m = min(stroke[1])
        if min_y is None or min_y > m:
            min_y = m

    return (min_x, max_x, min_y, max_y)


def draw_bounding_box(draw, obj, cx=0, cy=0, scale=1, colour="blue"):
    min_x, max_x, min_y, max_y = get_quickdraw_obj_bounds(obj)
    draw.rectangle(
        [
            (cx + min_x * scale, cy + min_y * scale),
            (cx + max_x * scale, cy + max_y * scale),
        ],
        outline=colour,
    )

