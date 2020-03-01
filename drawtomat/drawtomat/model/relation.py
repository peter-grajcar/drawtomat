

class Relation:
    """
     A class representing a relationship between two entities.

     Parameters
     ----------
     src : Entity
        The source entity.
     dst : Entity
        The destination entity.
     rel : Adposition
        The type of the relation.
    """
    src: 'Entity'
    dst: 'Entity'
    rel: 'Adposition'

    def __init__(self, src, dst, rel) -> None:
        """
        Initialises a new relation given source and destination entity, and an adposition describing
        the relation.

        Parameters
        ----------
        src : Entity
            The source entity.
        dst : Entity
            The destination entity.
        rel : Adposition
            The adposition describing the relation.
        """
        self.src = src
        self.dst = dst
        self.rel = rel


