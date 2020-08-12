from graphviz import Digraph

from .entity import Entity
from .group import Group
from .object import Object


class Scene:
    """
    An object representing a scene, i.e. container which holds entities (Objects, Groups).

    Attributes
    ----------
    group : Group
        Root group of the scene.
    entity_register: set
        Set of all entities present in the scene (not only direct descendants).
    """

    def __init__(self, entities=None) -> None:
        self.entity_register = set()

        self.group = Group(scene=self)
        if entities is not None:
            self.add_entities(*entities)

    def register(self, entity: 'Entity') -> None:
        """
        Registers an entity. Register of entities contains all entities present in the scene (not only
        direct descendants as opposed of the 'entities' list).

        Parameters
        ----------
        entity
            The entity to register

        Returns
        -------
        None
        """
        self.entity_register.add(entity)

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
        self.group.add_entity(entity)

    def add_entities(self, *entities) -> None:
        """
        Adds all entities passed as an argument.

        Parameters
        ----------
        entities
            A list of entities to add.

        Returns
        -------
        None
        """
        for entity in entities:
            self.group.add_entity(entity)

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
            A graph representation of the scene.
        """

        id_counter = 0
        entity_ids = dict()

        graph = Digraph("model", filename=filename)
        graph.graph_attr["rankdir"] = "LR"
        graph.graph_attr["compound"] = "true"
        graph.node_attr["shape"] = "record"
        graph.edge_attr["fontsize"] = "10"
        graph.graph_attr["size"] = "6,6!"

        def register(entity: 'Entity'):
            nonlocal id_counter
            if not entity in entity_ids:
                entity_ids[entity] = id_counter
                id_counter += 1

        def object_dot_repr(g: 'Digraph', obj: 'Object'):
            if obj.attributes:
                label = f"{obj.word}<font point-size='9'><br align='left'/>attrs:<br align='left'/>" + "<br align='left'/>".join(f" - {attr}" for attr in obj.attributes) + "</font>"
                g.node(f"entity_{entity_ids[obj]}", label="<" + label + ">")
            else:
                g.node(f"entity_{entity_ids[obj]}", label=obj.word)

        def group_dot_repr(g: 'Digraph', group: 'Group'):
            with g.subgraph(name="cluster_" + str(entity_ids[group])) as sub:
                sub.graph_attr["label"] = "group"
                for e in group.entities:
                    entity_dot_repr(sub, e)
                sub.node("entity_" + str(entity_ids[group]), style="invis", shape="point", label="")

        def entity_dot_repr(g: 'Digraph', entity: 'Entity'):
            register(entity)

            if type(entity) is Group:
                group_dot_repr(g, entity)
            if type(entity) is Object:
                object_dot_repr(g, entity)

            for rel in entity.relations_out:
                register(rel.dst)
                attrs = {}
                if type(rel.src) == Group:
                    attrs["ltail"] = f"cluster_{entity_ids[rel.src]}"
                if type(rel.dst) == Group:
                    attrs["rtail"] = f"cluster_{entity_ids[rel.dst]}"
                graph.edge(f"entity_{entity_ids[rel.src]}", f"entity_{entity_ids[rel.dst]}", label=rel.rel.name, **attrs)

        for entity in self.group.entities:
            entity_dot_repr(graph, entity)

        graph.save()
        return graph
