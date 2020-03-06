from drawtomat.model.entity import Entity


class Object(Entity):
    """
    An entity representing a single object in the scene.

    Parameters
    ----------
    word : str
        The word describing the object.
    """

    def __init__(self, word: str, container=None) -> None:
        """
        Initialises a new object with given word inside a container.

        """
        if container:
            super(Object, self).__init__(container)
        else:
            super(Object, self).__init__()
        self.word = word

    def __repr__(self) -> str:
        return f"ObjectEntity({self.word})"



