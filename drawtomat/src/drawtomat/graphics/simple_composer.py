import logging
from typing import List

from drawtomat.language.adposition import Adposition
from drawtomat.model.physical import PhysicalEntity, PhysicalObject, PhysicalGroup
from drawtomat.model.relational.group import Group
from drawtomat.model.relational.object import Object
from drawtomat.model.relational.scene import Scene


class SimpleComposer:
    """
    A simple scene composer.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def compose(self, scene: 'Scene') -> List[PhysicalEntity]:
        """
        Composes object from the scene into a list of wrapper objects.

        Parameters
        ----------
        scene
            The scene to compose.

        Returns
        -------
        List
            The list of physical entities
        """
        topological_order = _topological_order(scene.entity_register)

        self.logger.debug("=" * 80)
        self.logger.debug("Topological order: ", topological_order)

        #################################################################################
        # Step 1:   Go through the ordered list of entities and compute the dimensions  #
        #           of entities.                                                        #
        #################################################################################

        drawings = dict()
        default_size = 100  # default size of the object (in cm)
        unit = 1.5  # ?px = 1cm

        for entity in topological_order:
            if type(entity) == Group:
                physical_entity = PhysicalGroup(entity)
                # TODO: compute cumulative get_width() and get_height() of the group
                for child in entity.entities:
                    physical_entity.set_size(physical_entity.get_width() + drawings[child].get_width(),
                                             physical_entity.get_height() + drawings[child].get_height())
                drawings[entity] = physical_entity
            elif type(entity) == Object:
                physical_entity = PhysicalObject(entity, default_size=default_size, unit=unit)
                drawings[entity] = physical_entity

            self.logger.debug("\t", physical_entity)

        #################################################################################
        # Step 2:   Pop the entities from the ordered list and resolve the position of  #
        #           the entities.                                                       #
        #################################################################################
        for e in topological_order[::-1]:
            physical_entity = drawings[e]

            container = physical_entity.entity.container
            if container:
                physical_container = drawings[container]
                physical_entity.x = physical_container.x
                physical_entity.y = physical_container.y

            if physical_entity.entity.relations_out:
                rel = physical_entity.entity.relations_out[0]
                dst_wrapper = drawings[rel.dst]

                # adjust scale with respect to destination object
                if dst_wrapper.get_scale() < physical_entity.get_scale():
                    physical_entity.set_scale(dst_wrapper.get_scale())

                # adjust position with respect to the adposition defining the relation
                if rel.rel == Adposition.ON:
                    physical_entity.x = dst_wrapper.x
                    physical_entity.y = dst_wrapper.y - physical_entity.get_height() / 2 - dst_wrapper.get_height() / 2
                elif rel.rel == Adposition.ABOVE:
                    physical_entity.x = dst_wrapper.x
                    physical_entity.y = dst_wrapper.y - physical_entity.get_height() / 2 - dst_wrapper.get_height()
                elif rel.rel == Adposition.UNDER or rel.rel == Adposition.BELOW:
                    physical_entity.x = dst_wrapper.x
                    physical_entity.y = dst_wrapper.y + physical_entity.get_height() / 2 + dst_wrapper.get_height() / 2
                elif rel.rel == Adposition.NEXT_TO:
                    physical_entity.x = dst_wrapper.x + physical_entity.get_width() / 2 + dst_wrapper.get_width() / 2
                    physical_entity.y = dst_wrapper.y
                elif rel.rel == Adposition.BEHIND or rel.rel == Adposition.IN:

                    if rel.rel == Adposition.IN and (
                            physical_entity.get_width() > dst_wrapper.get_width() or
                            physical_entity.get_height() > dst_wrapper.get_height()
                    ):
                        padding = 2
                        q = min(dst_wrapper.get_width(), dst_wrapper.get_height()) / (
                                    max(physical_entity.get_width(), physical_entity.get_height()) * padding)
                        physical_entity.set_scale(q * physical_entity.get_scale())
                    if rel.rel == Adposition.BEHIND:
                        # make the object look smaller
                        physical_entity.set_scale(0.75)

                    # align centres of gravity
                    gx, gy = dst_wrapper.get_centre_of_gravity()
                    dx, dy = gx, gy

                    gx, gy = physical_entity.get_centre_of_gravity()
                    dx, dy = dx - gx, dy - gy

                    physical_entity.x, physical_entity.y = dst_wrapper.x + dx, dst_wrapper.y + dy

            if type(physical_entity) == PhysicalGroup:
                pass
            elif type(physical_entity) == PhysicalObject:
                pass

        return [v for v in drawings.values() if type(v) == PhysicalObject]


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
