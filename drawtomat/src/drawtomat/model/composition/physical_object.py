from drawtomat.model.composition.physical_entity import PhysicalEntity


class PhysicalObject(PhysicalEntity):
    """
    A wrapper type for object entity.

    Attributes
    ----------
    strokes: list
        object drawing strokes
    """

    def __init__(self, obj: 'Object') -> None:
        super(PhysicalObject, self).__init__(obj)
        self.strokes = []

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
