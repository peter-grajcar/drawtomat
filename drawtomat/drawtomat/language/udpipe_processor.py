import conllu
from ufal.udpipe import Model, Pipeline, ProcessingError

from drawtomat.language.adposition import Adposition
from drawtomat.model.group import Group
from drawtomat.model.object import Object
from drawtomat.model.scene import Scene
from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class UDPipeProcessor:
    """
    A description processor based on UDPipe.

    Attributes
    ----------
    model : Model
        UDPipe model.
    """

    def __init__(self, model_filename: str) -> None:
        self.model = Model.load(model_filename)
        if not self.model:
            raise Exception(f"Cannot load model from file \"{model_filename}\".")

    @staticmethod
    def _approach_a(parsed: 'list[TokenList]') -> Scene:
        """
        A naive approach of processing the description. Each noun is classified as an object.
        Two objects connected with 'and' are grouped into a group. An adposition between two
        entities is used to create a relation between the two entities.

        Parameters
        ----------
        parsed
            A list of sentences.

        Returns
        -------
        Scene
            Constructed scene.
        """
        scene = Scene()

        last_entity = None
        adp = None
        group = False

        for sentence in parsed:
            for token in sentence:
                if token["upostag"] == "NOUN":
                    unknown = False
                    if token["lemma"] in QuickDrawDataset.words():
                        print(f"object \"{token['lemma']}\"")
                    else:
                        print(f"unknown word: \"{token['form']}\"")
                        unknown = True

                    obj = Object(scene, word=(token["lemma"] + ("?" if unknown else "")), container=scene)

                    if last_entity and adp:
                        last_entity.make_relation(obj, adp)
                        adp = None
                    if last_entity and group:
                        g = Group(scene, container=scene)
                        scene.group.remove(last_entity)
                        scene.group.remove(obj)
                        g.add_entities(last_entity, obj)
                        group = False

                        last_entity = g
                        continue

                    last_entity = obj

                elif token["upostag"] == "ADP":
                    adp = Adposition.for_name(token["lemma"])
                    print(f"relation {adp.name}") if adp else print(f"unsupported relation \"{token['form']}\"")
                elif token["lemma"] == "and":
                    group = True

        return scene

    @staticmethod
    def _approach_b(parsed: 'list[TokenList]') -> Scene:
        """

        Parameters
        ----------
        parsed
            A list of sentences.

        Returns
        -------
        Scene
            Constructed scene.
        """
        scene = Scene()

        for sentence in parsed:
            root = sentence.to_tree()

            entity_stack = list()
            entity_stack_size = 0
            entity_stack_ptrs = dict()

            visited = set()
            node_stack = [root]
            node_stack_size = 1
            entity_position = dict()

            while node_stack_size:
                node = node_stack[-1]
                closing = False
                if node.token["id"] in visited:
                    # closing the node
                    node_stack.pop()
                    node_stack_size -= 1
                    closing = True
                else:
                    # opening the node
                    visited.add(node.token["id"])
                    for child in node.children[::-1]:
                        node_stack.append(child)
                        node_stack_size += 1

                token = node.token
                print("closing: " if closing else "opening: ", token["form"])

                if not closing:
                    entity_stack_ptrs[token["id"]] = entity_stack_size

                    if token["upostag"] == "NOUN" or token["upostag"] == "PROPN":
                        print(f"\tObject({token['lemma']})")
                        obj = None

                        # If a noun is preceded by 'the' try to find an existing object
                        # in scene's entity register.
                        # TODO: refactor this into separate method
                        for child in node.children:
                            if child.token["lemma"] == "the":
                                for e in scene.entity_register:
                                    if type(e) == Object and e.word == token["lemma"]:
                                        obj = e

                        if not obj:
                            obj = Object(scene, word=token["lemma"])

                        entity_stack.append(obj)
                        entity_stack_size += 1
                        entity_position[obj] = token["id"]

                    # Creates relation between two objects at the top of
                    # the stack
                    if token["upostag"] == "ADP":
                        print(f"\tRelation({token['lemma']})")
                        adp = Adposition.for_name(token["lemma"])

                        src = entity_stack[-2]
                        dst = entity_stack[-1]
                        if entity_position[src] > entity_position[dst]:
                            src, dst = dst, src

                        src.make_relation(dst, adp)

                else:
                    ptr = entity_stack_ptrs[token["id"]]
                    frame = entity_stack[ptr:]
                    frame_size = entity_stack_size - ptr
                    print(f"\tFrame:\t{frame}")

                    frame_set = set()
                    frame_set_size = 0
                    for e in frame:
                        if e.container is None:
                            frame_set.add(e)
                            frame_set_size += 1

                    print(f"\t\t{frame_set}")

                    # if there are at least two entities in the entity stack frame
                    # merge them into one group.
                    if frame_set_size > 1:
                        g = Group(scene, entities=frame_set)
                        entity_position[g] = max([entity_position[e] for e in frame])

                        del entity_stack[ptr:]
                        entity_stack.append(g)
                        entity_stack_size -= frame_size - 1

            # Put all entities which does not belong to any group to the scene
            for e in entity_stack:
                if e.container is None:
                    scene.add_entity(e)
            print("done")

        return scene

    def process(self, text: str) -> Scene:
        """
        Processes the description and builds a scene based on it.

        Parameters
        ----------
        text : str
            The description of the scene.

        Returns
        -------
        Scene
            The scene described by the text
        """
        pipeline = Pipeline(self.model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
        error = ProcessingError()
        processed = pipeline.process(text, error)
        parsed = conllu.parse(processed)

        print(processed)
        # print(parsed)

        # scene = self._approach_a(parsed)
        scene = self._approach_b(parsed)

        return scene
