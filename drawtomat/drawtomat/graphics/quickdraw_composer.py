import random

from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class _GroupWrapper:
    """
    A wrapper type for group entity.

    Attributes
    ----------
    entity: Group
        A reference to the original group from the model.
    width:
        Cumulative width of the group, i.e. the sum of widths of the entities in the group.
    height:
        Cumulative height of the group, i.e. the sum of height of the entities in the group.
    """

    def __init__(self, group: 'Group') -> None:
        self.entity = group
        self.width = 0
        self.height = 0


class _ObjectWrapper:
    """
    A wrapper type for object entity.

    Attributes
    ----------
    entity: Object
        A reference to the original object from the model.
    """

    def __init__(self, obj: 'Object') -> None:
        self.entity = obj
        self._load_drawing()

    def _load_drawing(self, adjust_size=0) -> list:
        """
        Loads a drawing from the Quick, Draw! dataset, crops the drawing and returns the strokes.
        Sets the boundary attributes of the wrapper (width, height) and adjusted strokes (in Quick, Draw! format).

        Returns
        -------
        list
            A list of strokes (in Quick, Draw! dataset format).
        """
        word = self.entity.word
        # TODO: handle KeyError for unknown words
        data = QuickDrawDataset.images(word)
        drawing = random.choice(data)["drawing"]

        min_x = min(stroke[1] for stroke in drawing)
        max_x = max(stroke[1] for stroke in drawing)
        min_y = min(stroke[2] for stroke in drawing)
        max_y = max(stroke[2] for stroke in drawing)

        width = max_x - min_x
        height = max_y - min_y

        if adjust_size:
            # TODO: choose dominant dimension
            q = max(width, height) / adjust_size
        else:
            q = 1

        self.strokes = [
            [
                stroke[0],                             # time
                [(x - min_x) / q for x in stroke[1]],  # x-axis
                [(y - min_y) / q for y in stroke[2]]   # y-axis
            ]
            for stroke in drawing
        ]
        self.width = width / q
        self.height = height / q


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
            The scene to compose.

        Returns
        -------
        list
            The list of strokes in format specified in (TODO: add reference to the format specification)
        """
        topological_order = self._topological_order(scene.entity_register)
        drawn = set()

        print("Topological order: ", topological_order)

        # Step 1:   Go through the ordered list of entities and compute the dimensions
        #           of entities.

        default_size = 100
        for entity in topological_order:
            pass

        # Step 2:   Pop the entities from the ordered list and resolve the position of
        #           the entities.
