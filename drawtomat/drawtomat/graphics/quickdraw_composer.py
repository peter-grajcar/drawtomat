from drawtomat.language.adposition import Adposition
from drawtomat.model.physical.physical_group import PhysicalGroup
from drawtomat.model.physical.physical_object import PhysicalObject
from drawtomat.model.relational.group import Group
from drawtomat.model.relational.object import Object
from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class QuickDrawComposer:
    """
    A scene composer based on "Quick, Draw!" data.
    """

    def __init__(self):
        self.dataset = QuickDrawDataset.words()

    def _topological_order(self, entity_register):
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

    def compose(self, scene: 'Scene') -> list:
        """
        Composes object from the scene into a list of wrapper objects.

        Parameters
        ----------
        scene
            The scene to compose.

        Returns
        -------
        list
            The list of wrapper objects
        """
        topological_order = self._topological_order(scene.entity_register)

        print("=" * 80)
        print("Topological order: ", topological_order)

        #################################################################################
        # Step 1:   Go through the ordered list of entities and compute the dimensions  #
        #           of entities.                                                        #
        #################################################################################

        drawings = dict()
        default_size = 100  # default size of the object (in cm)
        unit = 1.5            # ?px = 1cm

        for entity in topological_order:
            if type(entity) == Group:
                wrapper = PhysicalGroup(entity)
                # TODO: compute cumulative get_width() and get_height() of the group
                for child in entity.entities:
                    wrapper.set_dimensions(wrapper.get_width() + drawings[child].get_width(),
                                           wrapper.get_height() + drawings[child].get_height()
                                           )
                drawings[entity] = wrapper
            elif type(entity) == Object:
                wrapper = PhysicalObject(entity, default_size=default_size, unit=unit)
                drawings[entity] = wrapper

            print("\t", wrapper)

        #################################################################################
        # Step 2:   Pop the entities from the ordered list and resolve the position of  #
        #           the entities.                                                       #
        #################################################################################
        for e in topological_order[::-1]:
            wrapper = drawings[e]

            container = wrapper.entity.container
            if container:
                container_wrapper = drawings[container]
                wrapper.x = container_wrapper.x
                wrapper.y = container_wrapper.y

            if wrapper.entity.relations_out:
                rel = wrapper.entity.relations_out[0]
                dst_wrapper = drawings[rel.dst]

                # adjust scale with respect to destination object
                if dst_wrapper.get_scale() < wrapper.get_scale():
                    wrapper.set_scale(dst_wrapper.get_scale())

                # adjust position with respect to the adposition defining the relation
                if rel.rel == Adposition.ON:
                    wrapper.x = dst_wrapper.x
                    wrapper.y = dst_wrapper.y - wrapper.get_height() / 2 - dst_wrapper.get_height() / 2
                elif rel.rel == Adposition.ABOVE:
                    wrapper.x = dst_wrapper.x
                    wrapper.y = dst_wrapper.y - wrapper.get_height() / 2 - dst_wrapper.get_height()
                elif rel.rel == Adposition.UNDER or rel.rel == Adposition.BELOW:
                    wrapper.x = dst_wrapper.x
                    wrapper.y = dst_wrapper.y + wrapper.get_height() / 2 + dst_wrapper.get_height() / 2
                elif rel.rel == Adposition.NEXT_TO:
                    wrapper.x = dst_wrapper.x + wrapper.get_width() / 2 + dst_wrapper.get_width() / 2
                    wrapper.y = dst_wrapper.y
                elif rel.rel == Adposition.BEHIND or rel.rel == Adposition.IN:

                    if rel.rel == Adposition.IN and (
                            wrapper.get_width() > dst_wrapper.get_width() or
                            wrapper.get_height() > dst_wrapper.get_height()
                    ):
                        padding = 2
                        q = min(dst_wrapper.get_width(), dst_wrapper.get_height()) / (max(wrapper.get_width(), wrapper.get_height()) * padding)
                        wrapper.set_scale(q * wrapper.get_scale())
                    if rel.rel == Adposition.BEHIND:
                        # make the object look smaller
                        wrapper.set_scale(0.75)

                    # align centres of gravity
                    gx, gy = dst_wrapper.get_centre_of_gravity()
                    cx, cy = dst_wrapper.get_centre()
                    dx, dy = gx - cx, gy - cy

                    gx, gy = wrapper.get_centre_of_gravity()
                    cx, cy = wrapper.get_centre()
                    dx, dy = dx + cx - gx, dy + cy - gy

                    wrapper.x, wrapper.y = dst_wrapper.x + dx, dst_wrapper.y + dy

            if type(wrapper) == PhysicalGroup:
                pass
            elif type(wrapper) == PhysicalObject:
                pass

        return [v for v in drawings.values() if type(v) == PhysicalObject]
