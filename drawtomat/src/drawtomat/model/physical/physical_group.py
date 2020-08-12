from drawtomat.model.physical.physical_entity import PhysicalEntity


class PhysicalGroup(PhysicalEntity):
    """
    A wrapper type for group entity.
    """

    def __init__(self, group: 'Group') -> None:
        super(PhysicalGroup, self).__init__(group)

    def set_dimensions(self, width: 'float', height: 'float') -> None:
        """
        Sets group width and height.

        Parameters
        ----------
        width : float
            width of the object
        height : float
            height of the object

        Returns
        -------
        None
        """
        self._width = width
        self._height = height

