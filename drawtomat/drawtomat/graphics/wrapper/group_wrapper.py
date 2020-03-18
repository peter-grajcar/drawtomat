

class GroupWrapper:
    """
    A wrapper type for group entity.

    Attributes
    ----------
    entity: Group
        A reference to the original group from the model.
    _width : int
        Cumulative width of the group, i.e. the sum of widths of the entities in the group.
    _height : int
        Cumulative height of the group, i.e. the sum of height of the entities in the group.
    x : int
        Position, x-axis.
    y : int
        Position, y-axis.
    """

    def __init__(self, group: 'Group') -> None:
        self.entity = group
        self._width = 0
        self._height = 0
        self.x = 0
        self.y = 0

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height

    def __repr__(self) -> str:
        return self.entity.__repr__() + f"[w={self.width():.0f}, h={self.height():.0f}]"

