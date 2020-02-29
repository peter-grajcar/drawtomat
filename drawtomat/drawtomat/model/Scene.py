from typing import IO

from drawtomat.model import Entity


class Scene:
    """
    An object representing a scene, i.e. container which holds entities (Objects, Groups).

    Attributes
    ----------
    entities : list[Entity]
        The list of entities in the scene.
    """
    entities: list[Entity]

    def __init__(self):
        """
        Initialises an empty scene.
        """
        self.entities = []

    def add_entity(self, entity: Entity) -> None:
        """
        Adds a new entity to the scene

        Parameters
        ----------
        entity : Entity
            The entity to be added to the scene.

        Returns
        -------
        None
        """
        self.entities.append(entity)

    def export_dot(self, file: IO) -> None:
        """
        Exports the scene as a graph represented in the dot language.

        Parameters
        ----------
        file : IO
            The output file.

        Returns
        -------
        None
        """

        # TODO: implement this function

        pass
