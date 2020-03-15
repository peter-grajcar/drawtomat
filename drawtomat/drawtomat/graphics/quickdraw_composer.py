from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class QuickDrawComposer:
    """
    A scene composer based on "Quick, Draw!" data.
    """

    def __init__(self):
        self.dataset = QuickDrawDataset.words()

    def _topological_order(self, entity_register):
        no_incoming_edges = set(entity_register)
        for vertex in entity_register:
            if vertex.container:
                no_incoming_edges.discard(vertex.container)
            for rel in vertex.relations:
                no_incoming_edges.discard(rel.dst)

        visited = set()
        stack = []
        order = []
        q = list(no_incoming_edges)

        while q:
            v = q.pop()
            if v not in visited:
                visited.add(v)
                q.extend([rel.dst for rel in v.relations])
                if v.container:
                    q.append(v.container)

                while stack and v not in [rel.dst for rel in stack[-1].relations] + [stack[-1].container]:
                    order.append(stack.pop())
                stack.append(v)

        return stack + order[::-1]

    def compose(self, scene: 'Scene') -> list:
        """
        Composes object from the scene into a list of strokes.

        Parameters
        ----------
        scene

        Returns
        -------
        list
        """
        order = self._topological_order(scene.entity_register)
        drawn = set()

        print("Topological order: ", order)

        # Step 1:   Go through the ordered list of entities and compute the dimensions
        #           of entities.

        # Step 2:   Pop the entities from the ordered list and resolve the position of
        #           the entities.
