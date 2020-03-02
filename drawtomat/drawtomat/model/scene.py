from typing import IO

from drawtomat.model.entity import Entity
from drawtomat.model.group import Group
from drawtomat.model.object import Object


class Scene:
    """
    An object representing a scene, i.e. container which holds entities (Objects, Groups).

    Attributes
    ----------
    entities : list
        The list of entities in the scene.
    """
    entities: list

    def __init__(self) -> None:
        """
        Initialises an empty scene.
        """
        self.entities = []

    def add_entity(self, entity: 'Entity') -> None:
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

        id_counter = 0
        entity_ids = dict()
        for entity in self.entities:
            entity_ids[entity] = id_counter
            id_counter += 1

        def object_dot_repr(obj: 'Object'):
            print(f"Entity_{entity_ids[obj]} [label=\"{obj.word}\", shape=box];", file=file)
            for rel in obj.relations:
                print(f"Entity_{entity_ids[rel.src]} -> Entity_{entity_ids[rel.dst]} [label=\"{rel.rel.name}\"];", file=file)
                pass

        def group_dot_repr(group: 'Group'):
            print("subgraph Entity_" + str(entity_ids[group]) + " {", file=file)
            for e in group.group:
                entity_dot_repr(e)
                pass
            for rel in group.relations:
                # TODO:
                pass
            print("}", file=file)

        def entity_dot_repr(entity: 'Entity'):
            if type(entity) is Group:
                group_dot_repr(entity)
            if type(entity) is Object:
                object_dot_repr(entity)

        print("digraph Model {", file=file)
        for entity in self.entities:
            entity_dot_repr(entity)
        print("}", file=file)

        pass
