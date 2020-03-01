from abc import ABC

from drawtomat.model.relation import Relation


class Entity(ABC):
    """
    An abstract class representing an entity in a scene. An entity can relate to other entity via Relation.
    """

    relations: list

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
        self.relations.append(rel)
