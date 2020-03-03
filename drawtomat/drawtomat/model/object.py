from drawtomat.model.entity import Entity


class Object(Entity):
    """
    An entity representing a single object in the scene.

    Parameters
    ----------
    word : str
        The word describing the object.
    """

    def __init__(self, word: str) -> None:
        """
        Initialises a new object with given word.

        """
        super(Object, self).__init__()
        self.word = word

    def __init__(self, container, word: str) -> None:
        """
        Initialises a new object with given word inside a container.

        """
        super(Object, self).__init__(container)
        self.word = word



