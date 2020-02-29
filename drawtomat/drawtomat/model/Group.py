from drawtomat.model.Entity import Entity


class Group(Entity):
    """
    An entity representing a group of entities

    Parameters
    ----------
    group : list[Entity]
        The list of entities contained in the group.
    """
    group: list[Entity]

    def __init__(self) -> None:
        self.group = []

    def add_entity(self, entity: Entity) -> None:
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
        self.group.append(entity)


