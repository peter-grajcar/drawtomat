from .entity import Entity


class Object(Entity):
    """
    An entity representing a single object in the scene.

    Attributes
    ----------
    word : str
        The word describing the object.
    attributes : list
    """

    def __init__(self, scene: 'Scene', word: str, container=None) -> None:
        """
        Initialises a new object with given word inside a container.

        """
        if container:
            super(Object, self).__init__(scene, container=container)
        else:
            super(Object, self).__init__(scene)
        self.word = word
        self.attributes = list()

    def __repr__(self) -> str:
        return f"ObjectEntity({self.word})"



