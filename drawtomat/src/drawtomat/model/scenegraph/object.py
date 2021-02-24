from .entity import Entity
from .group import Group
from .relation import Relation


class Object(Entity):
    """
    An entity representing a single object in the scene.

    Attributes
    ----------
    word : str
        The word describing the object.
    attributes : list
    """

    def __init__(self, scene: 'Scene', word: str, container=None, attrs=None) -> None:
        """
        Initialises a new object with given word inside a container.

        """
        if container:
            super(Object, self).__init__(scene, container=container)
        else:
            super(Object, self).__init__(scene)
        self.word = word
        if attrs:
            self.attributes = attrs
        else:
            self.attributes = list()

    def make_relation(self, entity: 'Entity', adp: 'Adposition') -> None:
        if type(entity) == Object:
            rel = Relation(self, entity, adp)
            self.relations_out.append(rel)
            entity.relations_in.append(rel)
        elif type(entity) == Group:
            for e in entity.entities:
                rel = Relation(self, e, adp)
                self.relations_out.append(rel)
                e.relations_in.append(rel)

    def __repr__(self) -> str:
        return f"ObjectEntity({self.word})"
