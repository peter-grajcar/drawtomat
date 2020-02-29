from drawtomat.model.Entity import Entity


class Object(Entity):
    """
    An entity representing a single object in the scene.

    Parameters
    ----------
    word : str
        The word describing the object.
    """
    word: str

    def __init__(self, word: str) -> None:
        """
        Initialises a new object with given word.

        Parameters
        ----------
        word : str
            The word describing the object
        """
        self.word = word

