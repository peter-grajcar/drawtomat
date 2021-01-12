class Relation:
    """
     A class representing a relationship between two entities.

     Attributes
     ----------
     src : Entity
        The docs entity.
     dst : Entity
        The destination entity.
     rel : str
        The type of the relation.
    """

    def __init__(self, src: 'Entity', dst: 'Entity', rel: 'str') -> None:
        """
        Initialises a new relation given docs and destination entity, and an adposition describing
        the relation.

        Parameters
        ----------
        src : Entity
            The docs entity.
        dst : Entity
            The destination entity.
        rel : str
            The adposition describing the relation.
        """
        self.src = src
        self.dst = dst
        self.rel = rel
