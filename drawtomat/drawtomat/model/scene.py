from typing import IO

from graphviz import Digraph

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

    def export_dot(self, filename: str) -> Digraph:
        """
        Exports the scene as a graph represented in the dot language.

        Parameters
        ----------
        filename : str
            The output file name.

        Returns
        -------
        Digraph

        """

        id_counter = 0
        entity_ids = dict()

        def register(entity: 'Entity'):
            nonlocal id_counter
            if not entity_ids.get(entity):
                entity_ids[entity] = id_counter
                id_counter += 1

        def object_dot_repr(graph: 'Digraph', obj: 'Object'):
            graph.node(f"entity_{entity_ids[obj]}", label=obj.word)

        def group_dot_repr(graph: 'Digraph', group: 'Group'):
            with graph.subgraph(name="cluster_" + str(entity_ids[group])) as sub:
                for e in group.group:
                    entity_dot_repr(sub, e)
            graph.node("entity_" + str(entity_ids[group]), style="invis", shape="point", width=0, height=0, margin=0, label="")

        def entity_dot_repr(graph: 'Digraph', entity: 'Entity'):
            register(entity)

            if type(entity) is Group:
                group_dot_repr(graph, entity)
            if type(entity) is Object:
                object_dot_repr(graph, entity)

            for rel in entity.relations:
                register(rel.dst)
                attrs = ""
                # if type(rel.src) == Group:
                #    attrs += f"ltail=cluster_{entity_ids[rel.src]}, "
                # if type(rel.dst) == Group:
                #    attrs += f"rtail=cluster_{entity_ids[rel.dst]}, "
                graph.edge(f"entity_{entity_ids[rel.src]}", f"entity_{entity_ids[rel.dst]}", label=rel.rel.name)

        graph = Digraph("model", filename=filename)
        graph.graph_attr["rankdir"] = "LR"
        graph.graph_attr["compound"] = "true"
        graph.node_attr["shape"] = "record"
        for entity in self.entities:
            entity_dot_repr(graph, entity)

        graph.save()
        return graph
