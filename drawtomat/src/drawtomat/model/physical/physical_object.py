import random

from drawtomat.model.physical.physical_entity import PhysicalEntity
from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class PhysicalObject(PhysicalEntity):
    """
    A wrapper type for object entity.

    Attributes
    ----------
    strokes: list
        object drawing strokes
    """

    def __init__(self, obj: 'Object', default_size: int = 100, unit: float = 1) -> None:
        super(PhysicalObject, self).__init__(obj)
        self.strokes = []
        self._load_drawing(default_size=default_size, unit=unit)

    def _load_drawing(self, default_size: int = 100, unit: float = 1) -> None:
        """
        Loads a drawing from the Quick, Draw! dataset, crops the drawing and returns the strokes.
        Sets the boundary attributes of the wrapper (width, height) and adjusted strokes (in Quick, Draw! format).

        Returns
        -------
        list : List[List[List[int]]
            A list of strokes (in Quick, Draw! dataset format).
        """
        word = self.entity.word
        # TODO: handle KeyError for unknown words
        if not word in QuickDrawDataset.words():
            raise Exception(f"Unknown word \"{word}\".")

        data = QuickDrawDataset.images(word)
        drawing = random.choice(data)["drawing"]
        attrs = QuickDrawDataset.attributes(word)

        min_x = min([min(stroke[0]) for stroke in drawing])
        max_x = max([max(stroke[0]) for stroke in drawing])
        min_y = min([min(stroke[1]) for stroke in drawing])
        max_y = max([max(stroke[1]) for stroke in drawing])

        width = max_x - min_x
        height = max_y - min_y

        # TODO: load size of the object
        # TODO: choose dominant dimension
        if attrs["default_width"] and attrs["default_height"]:
            if attrs["default_width"] > attrs["default_height"]:
                q = unit * attrs["default_width"] / width
            else:
                q = unit * attrs["default_height"] / height
        elif attrs["default_width"]:
            q = unit * attrs["default_width"] / width
        elif attrs["default_height"]:
            q = unit * attrs["default_height"] / height
        else:
            q = unit * default_size / max(width, height)

        self.strokes = [
            [
                [(x - min_x - width/2) * q for x in stroke[0]],   # x-axis
                [(y - min_y - height/2) * q for y in stroke[1]],  # y-axis
                stroke[2],                                        # time
            ]
            for stroke in drawing
        ]

        self._width = width * q
        self._height = height * q

    def set_scale(self, scale: float) -> None:
        """
        Sets the scale of the object.

        Parameters
        ----------
        scale : float
            scale of the object

        Returns
        -------
        None
        """
        q = scale / self.get_scale()
        self.strokes = [
            [
                [(x * q) for x in stroke[0]],  # x-axis
                [(y * q) for y in stroke[1]],  # y-axis
                stroke[2],                     # time
            ]
            for stroke in self.strokes
        ]
        self._scale = scale

    def get_position(self) -> tuple:
        """
        Returns a position of the object in the scene.

        Returns
        -------
        tuple
        """
        return self.x, self.y

    def get_centre_of_gravity(self) -> tuple:
        """
        Computes the centre of gravity, i.e. averages the points of all strokes. The coordinates are relative.

        Returns
        -------
        tuple
            The centre of gravity of the object.
        """
        x = 0
        y = 0
        n = 0

        for stroke in self.strokes:
            x += sum(stroke[0])
            y += sum(stroke[1])
            n += len(stroke[2])

        x /= n
        y /= n
        return x, y

