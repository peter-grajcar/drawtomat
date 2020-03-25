from tkinter import Tk, Canvas, PhotoImage, Label

from drawtomat.graphics.quickdraw_composer import QuickDrawComposer
from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class QuickDrawRenderer:
    """
    An image renderer based on "Quick, Draw!" data.
    """

    def __init__(self):
        self.dataset = QuickDrawDataset.words()
        self.composer = QuickDrawComposer()

    def render(self, scene: 'Scene') -> None:
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

        composer = QuickDrawComposer()
        composition = composer.compose(scene)

        # ======== for debugging only ========
        root = Tk()
        root.title("Drawtomat")
        canvas = Canvas(root, width=600, height=400)
        canvas.pack()

        img = PhotoImage(file="output/model.dot.png")
        label = Label(root, image=img)
        label.pack()

        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for wrapper in composition:
            cx, cy = wrapper.get_centre()
            px, py = wrapper.x - cx, wrapper.y - cy
            # TODO: use width, height instead
            for stroke in wrapper.strokes:
                mx = min(stroke[0]) + px
                my = min(stroke[1]) + py
                if min_x is None or min_x > mx:
                    min_x = mx
                if min_y is None or min_y > my:
                    min_y = my

                mx = max(stroke[0]) + px
                my = max(stroke[1]) + py
                if max_x is None or max_x < mx:
                    max_x = mx
                if max_y is None or min_y < my:
                    max_y = my

        width = max_x - min_x
        height = max_y - min_y
        q = min(300 / width, 200 / height)

        for wrapper in composition:
            gx, gy = wrapper.get_centre_of_gravity()
            cx, cy = wrapper.get_centre()
            px, py = wrapper.x * q + 300 - cx * q, wrapper.y * q + 200 - cy * q

            for stroke in wrapper.strokes:
                if len(stroke[2]) < 2:
                    continue
                points = [(px + x*q, py + y*q) for (x, y) in zip(stroke[0], stroke[1])]
                canvas.create_line(*points)

            """
            canvas.create_rectangle(px, py, px + obj.get_width(), py + obj.get_height(), outline="#ff00ff")
            canvas.create_text(px + 4, py + 4, text=obj.entity.word, anchor="nw", fill="#ff00ff", font=("Courier", 10))
            canvas.create_line(px + gx - 4, py + gy, px + gx + 4, py + gy, fill="#ff00ff")
            canvas.create_line(px + gx, py + gy - 4, px + gx, py + gy + 4, fill="#ff00ff")
            canvas.create_line(px + cx - 3, py + cy - 3, px + cx + 3, py + cy + 3, fill="#00ffff")
            canvas.create_line(px + cx - 3, py + cy + 3, px + cx + 3, py + cy - 3, fill="#00ffff")
            """
        root.mainloop()
        # =====================================

