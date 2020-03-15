from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class QuickDrawComposer:
    """
    A scene composer based on "Quick, Draw!" data.
    """

    def __init__(self):
        self.dataset = QuickDrawDataset.words()

    def _topological_order(self, entity_list):
        visited = set()
        order = []
        stack = []

        q = list(entity_list)

        while q:
            v = q.pop()
            if v not in visited:
                visited.add(v)
                q.extend([rel.dst for rel in v.relations])

                while stack and v not in [rel.dst for rel in stack[-1].relations]:
                    order.append(stack.pop())
                stack.append(v)

        return stack + order

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
        order = self._topological_order(scene.entities)
        drawn = set()

        print("Topological order: ", order)
