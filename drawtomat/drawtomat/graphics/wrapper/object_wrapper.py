import random

from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class ObjectWrapper:
    """
    A wrapper type for object entity.

    Attributes
    ----------
    entity: Object
        A reference to the original object from the model.
    _width : int
        The width of the object.
    _height : int
        The height of the object.
    x : int
        Position, x-axis.
    y : int
        Position, y-axis.
    strokes: list

    scale: float
        A ratio between the default size and actual size.
    """

    def __init__(self, obj: 'Object', default_size: int = 100, unit: int = 1) -> None:
        self.entity = obj
        self.strokes = []
        self._width = 0
        self._height = 0
        self._load_drawing(default_size=default_size, unit=unit)
        self.x = 0
        self.y = 0
        self.scale = 1.0

    def _load_drawing(self, default_size: int = 100, unit: int = 1) -> list:
        """
        Loads a drawing from the Quick, Draw! dataset, crops the drawing and returns the strokes.
        Sets the boundary attributes of the wrapper (width, height) and adjusted strokes (in Quick, Draw! format).

        Returns
        -------
        list
            A list of strokes (in Quick, Draw! dataset format).
        """
        word = self.entity.word
        # TODO: handle KeyError for unknown words
        data = QuickDrawDataset.images(word)
        drawing = random.choice(data)["drawing"]

        min_x = min([min(stroke[0]) for stroke in drawing])
        max_x = max([max(stroke[0]) for stroke in drawing])
        min_y = min([min(stroke[1]) for stroke in drawing])
        max_y = max([max(stroke[1]) for stroke in drawing])

        width = max_x - min_x
        height = max_y - min_y
        # TODO: load size of the object
        # TODO: choose dominant dimension
        q = unit * default_size / max(width, height)

        self.strokes = [
            [
                [(x - min_x) * q for x in stroke[0]],  # x-axis
                [(y - min_y) * q for y in stroke[1]],  # y-axis
                stroke[2],                         # time
            ]
            for stroke in drawing
        ]

        self._width = width * q
        self._height = height * q

    def set_scale(self, scale: float):
        q = scale / self.scale
        self.strokes = [
            [
                [(x * q) for x in stroke[0]],  # x-axis
                [(y * q) for y in stroke[1]],  # y-axis
                stroke[2],                     # time
            ]
            for stroke in self.strokes
        ]
        self.scale = scale

    def width(self) -> float:
        """

        Returns
        -------

        """
        return self._width * self.scale

    def height(self) -> float:
        """

        Returns
        -------

        """
        return self._height * self.scale

    def position(self):
        """

        Returns
        -------

        """
        return self.x, self.y

    def centre_of_gravity(self):
        """
        Computes the centre of gravity, i.e. averages the points of all strokes. The coordinates are relative.

        Returns
        -------
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

    def centre(self):
        """
        Computes the centre of the object, i.e. centre of the bounding box. The coordinates are relative.

        Returns
        -------
            The centre of the object.
        """
        return self.width() / 2, self.height() / 2

    def __repr__(self) -> str:
        return self.entity.__repr__() + f"[w={self.width():.0f}, h={self.height():.0f}]"
