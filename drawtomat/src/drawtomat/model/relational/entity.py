import uuid
from abc import ABC

from drawtomat.language.adposition import Adposition
from .relation import Relation


class Entity(ABC):
    """
    An abstract class representing an entity in a scene. An entity can relate to other entity via Relation.

    Parameters
    ----------
    relations : list
        The list of relations.
    """

    def __init__(self, scene: 'Scene', container=None):
        self.relations_out = list()
        self.relations_in = list()
        self.container = container
        self.id = uuid.uuid1()
        if container:
            container.add_entity(self)

        scene.register(self)

    def make_relation(self, entity: 'Entity', adp: 'Adposition') -> None:
        """
        Creates a new Relation from the entity.

        Parameters
        ----------
        entity : Entity
            The destination entity.
        adp : Adposition
            The adposition describing the relation.

        Returns
        -------
        None
        """
        rel = Relation(self, entity, adp)
        self.relations_out.append(rel)
        entity.relations_in.append(rel)

    def __hash__(self) -> int:
        return self.id.__hash__()

