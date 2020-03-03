from drawtomat.model.entity import Entity


class Group(Entity):
    """
    An entity representing a group of entities

    Parameters
    ----------
    group : list
        The list of entities contained in the group.
    """

    def __init__(self) -> None:
        """
        Initialises an empty group.
        """
        super(Group, self).__init__()
        self.group = []

    def __init__(self, container) -> None:
        """
        Initialises an empty group inside a container.
        """
        super(Group, self).__init__(container)
        self.group = []

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
        self.group.append(entity)

    def add_entities(self, *entities) -> None:
        """


        Parameters
        ----------
        entities

        Returns
        -------
        None
        """
        for entity in entities:
            self.entities.append(entity)
