import drawtomat.model.relational
from drawtomat.model.physical.physical_entity import PhysicalEntity


class PhysicalGroup(PhysicalEntity):
    """
    A wrapper type for group entity.
    """

    def __init__(self, group: 'drawtomat.model.relational.Group') -> None:
        super(PhysicalGroup, self).__init__(group)

    def set_dimensions(self, width, height) -> None:
        """
        Sets group width and height.

        Parameters
        ----------
        width
        height

        Returns
        -------
        None
        """
        self._width = width
        self._height = height

