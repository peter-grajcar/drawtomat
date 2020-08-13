from tkinter import Tk, Canvas, PhotoImage, Label

import drawtomat.model.relational
from drawtomat.graphics.simple_composer import SimpleComposer
from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class SimpleRenderer:
    """
    A simple image renderer.
    """

    def __init__(self, show_bounds: bool = False):
        self.dataset = QuickDrawDataset.words()
        self.composer = SimpleComposer()
        self.show_bounds = show_bounds

    def render(self, scene: 'drawtomat.model.relational.Scene') -> None:
        """
        Renders a scene into an image.

        Parameters
        ----------
        scene
            The scene to render.

        Returns
        -------
        None
        """

        composer = SimpleComposer()
        composition = composer.compose(scene)

        # ======== for debugging only ========
        root = Tk()
        root.title("Drawtomat")
        canvas = Canvas(root, width=600, height=400)
        canvas.pack(side="left")
        img = PhotoImage(file="output/model.dot.png")
        label = Label(root, image=img, width=400, borderwidth=2, relief="solid")
        label.pack(fill="both", side="left")

        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for obj in composition:
            # TODO: use width, height instead
            for stroke in obj.strokes:
                mx = min(stroke[0]) + obj.x
                my = min(stroke[1]) + obj.y
                if min_x is None or min_x > mx:
                    min_x = mx
                if min_y is None or min_y > my:
                    min_y = my

                mx = max(stroke[0]) + obj.x
                my = max(stroke[1]) + obj.y
                if max_x is None or max_x < mx:
                    max_x = mx
                if max_y is None or min_y < my:
                    max_y = my

        width = max_x - min_x
        height = max_y - min_y
        q = min(300 / width, 200 / height)

        for obj in composition:
            gx, gy = obj.get_centre_of_gravity()
            gx, gy = gx * q, gy * q
            px, py = obj.x * q + 300, obj.y * q + 200

            for stroke in obj.strokes:
                if len(stroke[2]) < 2:
                    continue
                points = [(px + x*q, py + y*q) for (x, y) in zip(stroke[0], stroke[1])]
                canvas.create_line(*points)

            if self.show_bounds:
                canvas.create_rectangle(px, py, px + obj.get_width() * q, py + obj.get_height() * q, outline="#ff00ff")
                canvas.create_text(px + 4, py + 4, text=obj.entity.word, anchor="nw", fill="#ff00ff", font=("Courier", 10))
                canvas.create_line(px + gx - 4, py + gy, px + gx + 4, py + gy, fill="#ff00ff")
                canvas.create_line(px + gx, py + gy - 4, px + gx, py + gy + 4, fill="#ff00ff")
                canvas.create_line(px - 3, py - 3, px + 3, py + 3, fill="#00ffff")
                canvas.create_line(px - 3, py + 3, px + 3, py - 3, fill="#00ffff")

        root.mainloop()
        # =====================================

