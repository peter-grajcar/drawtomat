from tkinter import Tk, Canvas

from drawtomat.graphics.wrapper.group_wrapper import GroupWrapper
from drawtomat.graphics.wrapper.object_wrapper import ObjectWrapper
from drawtomat.language.adposition import Adposition
from drawtomat.model.group import Group
from drawtomat.model.object import Object
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

    def compose(self, scene: 'Scene') -> dict:
        """
        Composes object from the scene into a list of strokes.

        Parameters
        ----------
        scene
            The scene to compose.

        Returns
        -------
        list
            The list of strokes in format specified in (TODO: add reference to the format specification)
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
                wrapper = GroupWrapper(entity)
                # TODO: compute cumulative get_width() and get_height() of the group
                for child in entity.entities:
                    wrapper.set_dimensions(wrapper.get_width() + drawings[child].get_width(),
                                           wrapper.get_height() + drawings[child].get_height()
                                           )
                drawings[entity] = wrapper
            elif type(entity) == Object:
                wrapper = ObjectWrapper(entity, default_size=default_size, unit=unit)
                drawings[entity] = wrapper

            print("\t", wrapper)

        #################################################################################
        # Step 2:   Pop the entities from the ordered list and resolve the position of  #
        #           the entities.                                                       #
        #################################################################################

        # ======== for debugging only ========
        root = Tk()
        root.title("Drawtomat")
        canvas = Canvas(root, width=600, height=400)
        canvas.pack()

        def draw_obj(obj: 'ObjectWrapper'):
            gx, gy = obj.get_centre_of_gravity()
            cx, cy = obj.get_centre()
            px, py = obj.x + 300 - cx, obj.y + 200 - cy

            for stroke in obj.strokes:
                if len(stroke[2]) < 2:
                    continue
                points = [(px + x, py + y) for (x, y) in zip(stroke[0], stroke[1])]
                canvas.create_line(*points)

            """
            canvas.create_rectangle(px, py, px + obj.get_width(), py + obj.get_height(), outline="#ff00ff")
            canvas.create_text(px + 4, py + 4, text=obj.entity.word, anchor="nw", fill="#ff00ff", font=("Courier", 10))
            canvas.create_line(px + gx - 4, py + gy, px + gx + 4, py + gy, fill="#ff00ff")
            canvas.create_line(px + gx, py + gy - 4, px + gx, py + gy + 4, fill="#ff00ff")
            canvas.create_line(px + cx - 3, py + cy - 3, px + cx + 3, py + cy + 3, fill="#00ffff")
            canvas.create_line(px + cx - 3, py + cy + 3, px + cx + 3, py + cy - 3, fill="#00ffff")
            """

        # =====================================

        for e in topological_order[::-1]:
            wrapper = drawings[e]

            container = wrapper.entity.container
            if container:
                container_wrapper = drawings[container]
                dw = container_wrapper.get_width() - wrapper.get_width()
                dh = container_wrapper.get_height() - wrapper.get_height()
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
                elif rel.rel == Adposition.BEHIND or rel.rel == Adposition.IN:

                    if rel.rel == Adposition.IN and (
                            wrapper.get_width() < dst_wrapper.get_width() and
                            wrapper.get_height() < dst_wrapper.get_height()
                    ):
                        # TODO: compute the scale
                        wrapper.set_scale(0.5)

                    # align centres of gravity
                    gx, gy = dst_wrapper.get_centre_of_gravity()
                    cx, cy = dst_wrapper.get_centre()
                    dx, dy = gx - cx, gy - cy

                    gx, gy = wrapper.get_centre_of_gravity()
                    cx, cy = wrapper.get_centre()
                    dx, dy = dx + cx - gx, dy + cy - gy

                    wrapper.x, wrapper.y = dst_wrapper.x + dx, dst_wrapper.y + dy

            if type(wrapper) == GroupWrapper:
                pass
            elif type(wrapper) == ObjectWrapper:
                draw_obj(wrapper)

        # ======== for debugging only ========
        root.mainloop()
        # =====================================
