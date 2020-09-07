from tkinter import Tk, Canvas, PhotoImage, Label

import drawtomat.model.relational
from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class SimpleRenderer:
    """
    A simple image renderer.

    Attributes
    ----------
    dataset
    composer
    show_bounds : bool
    """

    def __init__(self, composer, show_bounds: bool = False):
        self.dataset = QuickDrawDataset.words()
        self.composer = composer
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

        composition = self.composer.compose(scene)

        # ======== for debugging only ========
        root = Tk()
        root.title("Drawtomat")
        canvas = Canvas(root, width=600, height=400, borderwidth=2, relief="solid")
        canvas.pack(side="top")
        img = PhotoImage(file="output/model.dot.png")
        label = Label(root, image=img, width=400, borderwidth=2, relief="solid")
        label.pack(fill="both", side="top")

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

        width = max_x - min_x + 50
        height = max_y - min_y + 50
        q = min(300 / width, 200 / height)

        for obj in composition:
            px, py = (obj.x - min_x + width/2) * q, (obj.y - min_y + height / 2) * q

            for stroke in obj.strokes:
                if len(stroke[2]) < 2:
                    continue
                points = [(px + x*q, py + y*q) for (x, y) in zip(stroke[0], stroke[1])]
                canvas.create_line(*points)

            if self.show_bounds:
                canvas.create_rectangle(px, py, px + obj.get_width() * q, py + obj.get_height() * q, outline="#ff00ff")
                canvas.create_text(px + 4, py + 4, text=obj.entity.word, anchor="nw", fill="#ff00ff", font=("Courier", 10))
                canvas.create_line(px - 4, py, px + 4, py, fill="#ff00ff")
                canvas.create_line(px, py - 4, px, py + 4, fill="#ff00ff")

        canvas.update()
        canvas.postscript(file="output/image.ps", colormode='color')


        root.mainloop()
        # =====================================

