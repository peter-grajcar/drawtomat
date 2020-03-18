from drawtomat.graphics.wrapper.entity_wrapper import EntityWrapper


class GroupWrapper(EntityWrapper):
    """
    A wrapper type for group entity.
    """

    def __init__(self, group: 'Group') -> None:
        super(GroupWrapper, self).__init__(group)

    def set_dimensions(self, width, height) -> None:
        """

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

