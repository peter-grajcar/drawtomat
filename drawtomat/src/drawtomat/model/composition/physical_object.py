from typing import Tuple


class PhysicalObject:
    """
    A wrapper type for object entity.

    Attributes
    ----------
    entity: Object
        A reference to the original entity from the scene graphs.
    _width : float
        Width of the entity (not scaled)
    _height : float
        Height of the entity (not scaled)
    x : float
        Position, x-axis.
    y : float
        Position, y-axis.
    _scale: float
        A ratio between the default size and actual size.
    strokes: list
        object drawing strokes

    """

    def __init__(self, obj: 'Object') -> None:
        self.entity = obj
        self.x = 0
        self.y = 0
        self._scale = 1
        self._width = 0
        self._height = 0
        self.strokes = []

    def __repr__(self) -> str:
        return self.entity.__repr__() + f"[w={self.get_width():.0f}, h={self.get_height():.0f}, x={self.x:.0f}, y={self.y:.0f}]"

    def get_width(self) -> float:
        """
        Returns the scaled width of the object.

        Returns
        -------
        float
            The width of the object.
        """
        return self._width * self._scale

    def get_height(self) -> float:
        """
        Returns the scaled height of the object.

        Returns
        -------
        float
            The height of the object.
        """
        return self._height * self._scale

    def get_size(self) -> Tuple[float, float]:
        """
        Returns the scaled width and height of the object.

        Returns
        -------
        tuple
            Width and height of the object
        """
        return self.get_width(), self.get_height()

    def get_scale(self) -> float:
        """
        Returns the scale of the object.

        Returns
        -------
        float
            The scale of the object.
        """
        return self._scale

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
                stroke[2],  # time
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

    def set_position(self, x: float, y: float) -> None:
        """
        Sets a new position.

        Parameters
        ----------
        x : float
            x coordinate
        y : float
            y coordinate

        Returns
        -------
        None
        """
        self.x = x
        self.y = y

    def get_relative_strokes(self) -> list:
        """
        TODO

        Returns
        -------
        list
            list of stroke coordinates relative to the object position
        """
        return [
            [
                [(x + self.x) for x in stroke[0]],  # x-axis
                [(y + self.y) for y in stroke[1]],  # y-axis
                stroke[2],  # time
            ]
            for stroke in self.strokes
        ]

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
