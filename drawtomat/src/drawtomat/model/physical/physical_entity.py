from abc import ABC


class PhysicalEntity(ABC):
    """
        An abstract wrapper type for entities.

        Attributes
        ----------
        entity: Group
            A reference to the original entity from the model.
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
        """

    def __init__(self, entity: 'Entity'):
        self.entity = entity
        self.x = 0
        self.y = 0
        self._scale = 1
        self._width = 0
        self._height = 0

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

    def get_size(self) -> tuple:
        """
        Returns the scaled width and height of the object.

        Returns
        -------
        tuple
            Width and height of the object
        """
        return self.get_width(), self.get_height()

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
            scale of the entity

        Returns
        -------
        None
        """
        self._scale = scale

    def get_centre_of_gravity(self) -> tuple:
        """
        By default returns the centre of a bounding box (same as get_centre).

        Returns
        -------
        tuple
            coordinates of the centre of gravity
        """
        return 0, 0

    def __repr__(self) -> str:
        return self.entity.__repr__() + f"[w={self.get_width():.0f}, h={self.get_height():.0f}, x={self.x:.0f}, y={self.y:.0f}]"
