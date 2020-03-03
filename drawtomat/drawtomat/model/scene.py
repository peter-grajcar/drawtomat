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

        def register(entity: 'Entity'):
            nonlocal id_counter
            if not entity_ids.get(entity):
                entity_ids[entity] = id_counter
                id_counter += 1

        def object_dot_repr(obj: 'Object'):
            print(f"entity_{entity_ids[obj]} [label=\"{obj.word}\"];", file=file)

        def group_dot_repr(group: 'Group'):
            print("subgraph cluster_" + str(entity_ids[group]) + " {", file=file)
            for e in group.group:
                entity_dot_repr(e)
            print("entity_" + str(entity_ids[group]) + " [style=invis, shape=point, width=0, height=0, margin=0, label=\"\"];", file=file)
            print("}", file=file)

        def entity_dot_repr(entity: 'Entity'):
            register(entity)

            if type(entity) is Group:
                group_dot_repr(entity)
            if type(entity) is Object:
                object_dot_repr(entity)

            for rel in entity.relations:
                register(rel.dst)
                attrs = ""
                if type(rel.src) == Group:
                    attrs += f"ltail=cluster_{entity_ids[rel.src]}, "
                if type(rel.dst) == Group:
                    attrs += f"rtail=cluster_{entity_ids[rel.dst]}, "
                print(f"entity_{entity_ids[rel.src]} -> entity_{entity_ids[rel.dst]} [label=\"{rel.rel.name}\", {attrs}];", file=file)

        print("digraph model {", file=file)
        print("graph [compound=true, rankdir=LR];", file=file)
        print("node [shape=record];", file=file)
        for entity in self.entities:
            entity_dot_repr(entity)
        print("}", file=file)

        pass
