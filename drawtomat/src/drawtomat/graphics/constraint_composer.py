import logging
from typing import List, Optional

import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.constraints import InsideConstraint, OnConstraint, DisjunctionConstraint, SideConstraint
from drawtomat.constraints import SklearnConstraint
from drawtomat.constraints.box_constraint import BoxConstraint
from drawtomat.language import Adposition
from drawtomat.model.physical import PhysicalEntity, PhysicalObject
from drawtomat.model.physical.physical_object_factory import PhysicalObjectFactory
from drawtomat.model.relational.group import Group
from drawtomat.model.relational.object import Object
from drawtomat.model.relational.scene import Scene


class ConstraintComposer:
    def __init__(self, obj_factory: 'PhysicalObjectFactory', use_ml: 'bool' = False):
        self.obj_factory = obj_factory
        self.use_ml = use_ml

    """
    Composer which uses geometrical constraints from `drawtomat.constraints` to place objects.

    See Also
    --------
    drawtomat.constraints
    """

    @staticmethod
    def _place_object(obj: 'PhysicalObject', constraints: 'List[Constraint]', point_limit: int = 5000) -> None:
        """

        Parameters
        ----------
        obj : PhysicalObject

        constraints : List[Constraint]

        point_limit : int

        Returns
        -------
        None
        """
        obj_size = max(obj.get_size())

        if not constraints:
            rand_point = np.random.normal(scale=obj_size, size=2)
            obj.set_position(rand_point[0], rand_point[1])
            return

        constraint_objs = [constraint.obj for constraint in constraints]

        for constraint in constraints:
            constraint.init()

        centres = np.array([centre.get_position() for centre in np.random.choice(constraint_objs, size=point_limit)])
        xs = np.random.normal(scale=obj_size, size=point_limit) + centres[:, 0]
        ys = np.random.normal(scale=obj_size, size=point_limit) + centres[:, 1]

        constraints_satisfied = np.zeros(shape=point_limit)

        for constraint in constraints:
            constraints_satisfied += constraint(xs, ys)

        best_point = np.argmax(constraints_satisfied)

        obj.set_position(xs[best_point], ys[best_point])

    def _get_constraints(self, adposition: 'Adposition', obj: 'PhysicalObject') -> 'Optional[Constraint]':
        if self.use_ml:
            return SklearnConstraint(obj, adposition.name.replace("_", " "))

        if adposition is Adposition.IN:
            return InsideConstraint(obj)
        elif adposition is Adposition.INSIDE:
            return InsideConstraint(obj)
        elif adposition is Adposition.INSIDE_OF:
            return InsideConstraint(obj)
        elif adposition is Adposition.ON:
            return OnConstraint(obj)
        elif adposition is Adposition.UNDER:
            return SideConstraint(obj, direction=(0, 1))
        elif adposition is Adposition.BELOW:
            return SideConstraint(obj, direction=(0, 1))
        elif adposition is Adposition.ABOVE:
            return SideConstraint(obj, direction=(0, -1))
        elif adposition is Adposition.BEHIND:
            return BoxConstraint(obj, scale=0.75)
        elif adposition is Adposition.IN_FRONT_OF:
            return BoxConstraint(obj, scale=1.5)
        elif adposition is Adposition.NEXT_TO:
            return DisjunctionConstraint(obj, [
                SideConstraint(obj, direction=(-1, 0), padding=10),
                SideConstraint(obj, direction=(1, 0), padding=10)
            ])
        # default
        return DisjunctionConstraint(obj, [
            SideConstraint(obj, direction=(-1, 0), padding=10),
            SideConstraint(obj, direction=(1, 0), padding=10),
            SideConstraint(obj, direction=(0, 1), padding=10),
            SideConstraint(obj, direction=(0, -1), padding=10),
        ])

    def compose(self, scene: 'Scene') -> List[PhysicalEntity]:
        """
        Creates a composition of objects in a scene.

        Parameters
        ----------
        scene : Scene
            the scene to compose

        Returns
        -------
        List[PhysicalEntity]
            composition
        """
        topological_order = _topological_order(scene.entity_register)

        physical_entities = dict()
        default_size = 100  # default size of the object (in cm)
        unit = 1.5  # ?px = 1cm

        # Create physical objects
        for entity in topological_order[::-1]:
            if type(entity) == Group:
                # TODO:
                pass
            elif type(entity) == Object:
                physical_entity = self.obj_factory.get_physical_object(entity, default_size=default_size, unit=unit)
                constraints = []
                for rel in entity.relations_out:
                    dst_obj = physical_entities[rel.dst]["obj"]
                    constraints.append(self._get_constraints(rel.rel, dst_obj))
                physical_entities[entity] = {"obj": physical_entity, "constraints": constraints}

        for entity in topological_order[::-1]:
            # all objects contained in a group will inherit all
            # group's constraint
            if type(entity) == Group:
                # accumulate group constraints
                constraints = []
                for rel in entity.relations_out:
                    dst_obj = physical_entities[rel.dst]["obj"]
                    constraints.append(self._get_constraints(rel.rel, dst_obj))
                # add constraints to objects in the group
                for e in entity.entities:
                    if type(e) == Object:
                        physical_entities[e]["constraints"].extend(constraints)
            elif type(entity) == Object:
                physical_entity = physical_entities[entity]
                self._place_object(physical_entity["obj"], physical_entity["constraints"])

                logging.getLogger(ConstraintComposer.__name__).debug(f"{physical_entity}")

        return [v["obj"] for v in physical_entities.values()]


def _topological_order(entity_register):
    no_incoming_edges = [e for e in entity_register if not e.relations_in]

    visited = set()
    stack = []
    order = []
    q = list(no_incoming_edges)

    while q:
        v = q.pop()
        if v not in visited:
            visited.add(v)
            q.extend([rel.dst for rel in v.relations_out])
            if v.container:
                q.append(v.container)

            while stack and v not in [rel.dst for rel in stack[-1].relations_out] + [stack[-1].container]:
                order.append(stack.pop())
            stack.append(v)

    return stack + order[::-1]
