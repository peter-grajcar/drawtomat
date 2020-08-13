from typing import List

import numpy as np

from drawtomat.constraints import Constraint
from drawtomat.constraints import InsideConstraint, OnConstraint, SideConstraint
from drawtomat.language import Adposition
from drawtomat.model.physical import PhysicalEntity, PhysicalObject, PhysicalGroup
from drawtomat.model.relational.group import Group
from drawtomat.model.relational.object import Object
from drawtomat.model.relational.scene import Scene


class ConstraintComposer:
    """
    Composer which uses geometrical constraints from `drawtomat.constraints` to place objects.

    See Also
    --------
    drawtomat.constraints
    """

    def _place_object(self, obj: 'PhysicalObject', constraints: 'List[Constraint]', point_limit: int = 1000) -> None:
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

        best_point = {"score": None, "point": None}
        num_of_constraints = len(constraints)
        centre = (
            sum([constraint.obj.x for constraint in constraints]) / num_of_constraints,
            sum([constraint.obj.y for constraint in constraints]) / num_of_constraints
        )

        for i in range(point_limit):
            rand_point = np.random.normal(scale=obj_size, size=2) + np.array(centre)
            constraints_satisfied = 0

            for constraint in constraints:
                constraints_satisfied += constraint(rand_point[0], rand_point[1])

            percentage = constraints_satisfied / num_of_constraints

            if best_point["score"] is None or best_point["score"] < percentage:
                best_point = {"score": percentage, "point": rand_point}
            if constraints_satisfied == num_of_constraints:
                break

        print(best_point)
        obj.set_position(best_point["point"][0], best_point["point"][1])

    def _get_constraints(self, adposition: 'Adposition', obj: 'PhysicalObject') -> List[Constraint]:
        if adposition is Adposition.IN:
            return [InsideConstraint(obj)]
        elif adposition is Adposition.INSIDE:
            return [InsideConstraint(obj)]
        elif adposition is Adposition.ON:
            return [OnConstraint(obj)]
        elif adposition is Adposition.NEXT_TO:
            return [
                SideConstraint(obj, direction=(-1, 0)),
                SideConstraint(obj, direction=(1, 0))
            ]

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

        physical_entities = []
        default_size = 100  # default size of the object (in cm)
        unit = 1.5  # ?px = 1cm

        # Create physical entities while maintaining
        # the topological order
        for entity in topological_order[::-1]:
            if type(entity) == Group:
                physical_entity = PhysicalGroup(entity)

                physical_entities.append(physical_entity)
            elif type(entity) == Object:
                physical_entity = PhysicalObject(entity, default_size=default_size, unit=unit)
                physical_entities.append(physical_entity)

            print("\t", physical_entity)

        for entity in physical_entities:
            pass

        return  # TODO


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
