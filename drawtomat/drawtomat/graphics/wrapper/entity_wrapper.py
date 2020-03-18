from abc import ABC


class EntityWrapper(ABC):
    """
        An abstract wrapper type for entities.

        Attributes
        ----------
        entity: Group
            A reference to the original group from the model.
        _width : float
            Cumulative width of the group, i.e. the sum of widths of the entities in the group.
        _height : float
            Cumulative height of the group, i.e. the sum of height of the entities in the group.
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

    def get_width(self) -> float:
        """

        Returns
        -------
        float
        """
        return self._width * self._scale

    def get_height(self) -> float:
        """

        Returns
        -------
        float
        """
        return self._height * self._scale

    def get_scale(self) -> float:
        """

        Returns
        -------
        float
        """
        return self._scale

    def set_scale(self, scale: float) -> None:
        """

        Parameters
        ----------
        scale

        Returns
        -------
        None
        """
        self._scale = scale

    def __repr__(self) -> str:
        return self.entity.__repr__() + f"[w={self.get_width():.0f}, h={self.get_height():.0f}]"
