from PIL import Image, ImageDraw

import drawtomat.model.scenegraph
from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class SimpleRenderer:
    """
    A simple image renderer. Renders the scene using Pillow.

    Attributes
    ----------
    composer
        composer which will be used during the rendering.
    show_bounds : bool
        if true, a bounding box will be rendered around each object.
    """

    def __init__(self, composer, show_bounds: bool = False):
        self.dataset = QuickDrawDataset.words()
        self.composer = composer
        self.show_bounds = show_bounds

    def render(self, scene: 'drawtomat.model.scenegraph.Scene') -> None:
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

        im_w, im_h = 600, 600
        im = Image.new("RGB", (im_w, im_h), "white")
        draw = ImageDraw.Draw(im)

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
        q = min(im_w / width / 2, im_h / height / 2)

        for obj in composition:
            px, py = (obj.x - min_x + width / 2) * q, (obj.y - min_y + height / 2) * q

            for stroke in obj.strokes:
                if len(stroke[2]) < 2:
                    continue
                points = [(px + x * q, py + y * q) for (x, y) in zip(stroke[0], stroke[1])]
                draw.line(points, fill="black")

            if self.show_bounds:
                draw.rectangle([px, py, px + obj.get_width() * q, py + obj.get_height() * q], outline="#ff00ff")
                draw.text([px + 4, py + 4], text=obj.entity.word, anchor="nw", fill="#ff00ff", font=("Courier", 10))
                draw.line([px - 4, py, px + 4, py], fill="#ff00ff")
                draw.line([px, py - 4, px, py + 4], fill="#ff00ff")

        im.show()
