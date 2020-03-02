from drawtomat.model.entity import Entity


class Object(Entity):
    """
    An entity representing a single object in the scene.

    Parameters
    ----------
    word : str
        The word describing the object.
    """

    def __init__(self, scene: 'Scene', word: str) -> None:
        """
        Initialises a new object with given word.

        Parameters
        ----------
        word : str
            The word describing the object
        """
        super(Object, self).__init__(scene)
        self.word = word



