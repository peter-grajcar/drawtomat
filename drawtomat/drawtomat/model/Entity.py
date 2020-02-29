from abc import ABC

from drawtomat.language.Adposition import Adposition
from drawtomat.model.Relation import Relation


class Entity(ABC):
    """
    An abstract class representing an entity in a scene. An entity can relate to other entity via Relation.
    """

    relations: list[Relation]

    def make_relation(self, entity: 'Entity', adposition: Adposition) -> None:
        """
        Creates a new Relation from the entity.

        Parameters
        ----------
        entity : Entity
            The destination entity.
        adposition : Adposition
            The adposition describing the relation.

        Returns
        -------
        None
        """
        rel = Relation(self, entity, adposition)
        self.relations.append(rel)
