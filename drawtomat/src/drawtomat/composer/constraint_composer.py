import logging
from typing import List, Tuple

import numpy as np

from drawtomat.composer.factory.physical_object_factory import PhysicalObjectFactory
from drawtomat.composer.scaler.physical_object_scaler import PhysicalObjectScaler
from drawtomat.constraints import ClassifierConstraint
from drawtomat.constraints import Constraint
from drawtomat.constraints import InsideConstraint, OnConstraint, DisjunctionConstraint, SideConstraint
from drawtomat.constraints.box_constraint import BoxConstraint
from drawtomat.model.composition import PhysicalObject
from drawtomat.model.scenegraph.group import Group
from drawtomat.model.scenegraph.object import Object
from drawtomat.model.scenegraph.scene import Scene


class ConstraintComposer:
    """
    Composer which uses geometrical constraints from `drawtomat.constraints` to place objects.

    See Also
    --------
    drawtomat.constraints
    """

    def __init__(self, obj_factory: 'PhysicalObjectFactory', obj_scaler: 'PhysicalObjectScaler',
                 use_ml: 'bool' = False):
        self.obj_factory = obj_factory
        self.obj_scaler = obj_scaler
        self.use_ml = use_ml

    @staticmethod
    def _place_object(obj: 'PhysicalObject', constraints: 'List[Constraint]', point_limit: int = 5000) -> None:
        """
        Places object using monte carlo algorithm.

        Parameters
        ----------
        obj : PhysicalObject
            object to place.

        constraints : List[Constraint]
            list of object's constraints.

        point_limit : int
            number of randomly generated points.

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

    def _scale_object(self, sub: 'PhysicalObject', obj_pred: 'List[Tuple[PhysicalObject, str]]') -> None:
        """
        Scales given object using the composer's scaler.

        Parameters
        ----------
        sub
            An object to scale.

        obj_pred
            List of (object, predicate) pairs which represent relations with
            other objects in the scene.

        Returns
        -------
        None
        """
        if not obj_pred:
            return

        logging.getLogger(ConstraintComposer.__name__).debug(f"scaling using {self.obj_scaler.__class__.__name__}")
        logging.getLogger(ConstraintComposer.__name__).debug(f"scaling {sub.entity.word} wrt: {obj_pred}")

        scale = 0
        for obj, pred in obj_pred:
            scale += self.obj_scaler.scale(sub, obj, pred)
        scale /= len(obj_pred)

        logging.getLogger(ConstraintComposer.__name__).debug(f"scale = {scale}")

        sub.set_scale(scale)

    def _get_constraints(self, adposition: 'str', obj: 'PhysicalObject') -> 'Constraint':
        """
        Returns a constraint object for given adposition.

        Parameters
        ----------
        adposition

        obj

        Returns
        -------
        Constraint

        """
        if self.use_ml:
            return ClassifierConstraint(obj, adposition)

        if adposition == "IN":
            return InsideConstraint(obj, adposition)
        elif adposition == "INSIDE":
            return InsideConstraint(obj, adposition)
        elif adposition == "INSIDE OF":
            return InsideConstraint(obj, adposition)
        elif adposition == "ON":
            return OnConstraint(obj, adposition)
        elif adposition == "UNDER":
            return SideConstraint(obj, adposition, direction=(0, 1))
        elif adposition == "BELOW":
            return SideConstraint(obj, adposition, direction=(0, 1))
        elif adposition == "ABOVE":
            return SideConstraint(obj, adposition, direction=(0, -1))
        elif adposition == "BEHIND":
            return BoxConstraint(obj, adposition, scale=0.75)
        elif adposition == "IN FRONT OF":
            return BoxConstraint(obj, adposition, scale=1.5)
        elif adposition == "NEXT TO":
            return DisjunctionConstraint(obj, adposition, [
                SideConstraint(obj, adposition, direction=(-1, 0), padding=10),
                SideConstraint(obj, adposition, direction=(1, 0), padding=10)
            ])
        # default
        return DisjunctionConstraint(obj, adposition, [
            SideConstraint(obj, adposition, direction=(-1, 0), padding=10),
            SideConstraint(obj, adposition, direction=(1, 0), padding=10),
            SideConstraint(obj, adposition, direction=(0, 1), padding=10),
            SideConstraint(obj, adposition, direction=(0, -1), padding=10),
        ])

    def compose(self, scene: 'Scene') -> List[PhysicalObject]:
        """
        Creates a composition of objects in a scene.

        Parameters
        ----------
        scene : Scene
            The scene to compose

        Returns
        -------
        List[PhysicalObject]
            A composition.
        """
        topological_order = _topological_order(scene.entity_register)

        physical_entities = dict()
        default_size = 100  # default size of the object (in cm)
        unit = 1.5  # ?px = 1cm

        logging.getLogger(ConstraintComposer.__name__).debug(topological_order)

        # Create composition objects
        for entity in topological_order[::-1]:
            if type(entity) == Group:
                pass
            elif type(entity) == Object:
                physical_entity = self.obj_factory.get_physical_object(entity, default_size=default_size, unit=unit)
                constraints = []
                for rel in entity.relations_out:
                    # TODO: case where dst_obj is a group
                    if type(rel.dst) == Object:
                        dst_obj = physical_entities[rel.dst]["obj"]
                        constraints.append(self._get_constraints(rel.rel, dst_obj))
                physical_entities[entity] = {"obj": physical_entity, "constraints": constraints}

        last_sub = None
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
                sub = physical_entities[entity]

                # object predicate pairs
                obj_pred = [(constraint.obj, constraint.pred) for constraint in sub["constraints"]]
                if not obj_pred and last_sub:
                    obj_pred = [(last_sub["obj"], None)]

                self._scale_object(sub["obj"], obj_pred)
                self._place_object(sub["obj"], sub["constraints"])

                last_sub = sub

                logging.getLogger(ConstraintComposer.__name__).debug(f"{sub}")

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
