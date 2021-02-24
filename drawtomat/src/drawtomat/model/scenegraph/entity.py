import uuid
from abc import ABC, abstractmethod
from typing import List

from .relation import Relation


class Entity(ABC):
    """
    An abstract class representing an entity in a scene. An entity can relate to other entity via Relation.

    Attributes
    ----------
    relations_in : List[Relation]

    relations_out : List[Relation]

    container : Entity

    id : uuid.UUID
    """

    def __init__(self, scene: 'Scene', container=None):
        self.relations_out = list()
        self.relations_in = list()
        self.container = container
        self.id = uuid.uuid1()
        if container:
            container.add_entity(self)

        scene.register(self)

    @abstractmethod
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
        pass

    def __hash__(self) -> int:
        return self.id.__hash__()
