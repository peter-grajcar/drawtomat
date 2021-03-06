from typing import List

from .entity import Entity


class Group(Entity):
    """
    An entity representing a group of entities

    Attributes
    ----------
    group : List[Entity]
        The list of entities contained in the group.
    """

    def __init__(self, scene: 'Scene', container=None, entities=None) -> None:
        if container:
            super(Group, self).__init__(scene, container=container)
        else:
            super(Group, self).__init__(scene)

        self.entities = list()
        if entities is not None:
            self.add_entities(*entities)
        self.container = container

    def add_entity(self, entity: 'Entity') -> None:
        """
        Adds a new entity to the group.

        Parameters
        ----------
        entity : Entity
            The entity to be added to the group.

        Returns
        -------
        None
        """
        self.entities.append(entity)
        entity.container = self

    def add_entities(self, *entities) -> None:
        """
        Adds new entities to the group.

        Parameters
        ----------
        entities : Iterable[Entity]
            The entities to be added to the group.

        Returns
        -------
        None
        """
        for entity in entities:
            self.entities.append(entity)
            entity.container = self

    def make_relation(self, entity: 'Entity', adp: 'Adposition') -> None:
        for e in self.entities:
            e.make_relation(entity, adp)

    def __repr__(self) -> str:
        return f"GroupEntity({len(self.entities)})"
