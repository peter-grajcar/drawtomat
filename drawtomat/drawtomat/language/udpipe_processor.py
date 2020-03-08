from queue import Queue

import conllu
from ufal.udpipe import Model, Pipeline, ProcessingError

from drawtomat.language.adposition import Adposition
from drawtomat.model.group import Group
from drawtomat.model.object import Object
from drawtomat.model.relation import Relation
from drawtomat.model.scene import Scene
from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class UDPipeProcessor:
    """
    A description processor based on UDPipe.
    """
    model: Model

    def __init__(self, model_filename: str) -> None:
        """
        Initialises a new UDPipe processor from model file.

        Parameters
        ----------
        model_filename
            UDPipe model.
        """
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

                    obj = Object(token["lemma"] + ("?" if unknown else ""), container=scene)

                    if last_entity and adp:
                        last_entity.make_relation(obj, adp)
                        adp = None
                    if last_entity and group:
                        g = Group(container=scene)
                        scene.entities.remove(last_entity)
                        scene.entities.remove(obj)
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

        entity_stack = []
        entity_stack_size = 0
        entity_stack_ptrs = {}

        for sentence in parsed:
            root = sentence.to_tree()

            visited = set()
            primary_stack = [root]
            primary_stack_size = 1

            while primary_stack_size:
                node = primary_stack[-1]
                closing = False
                if node.token["id"] in visited:
                    # closing the node
                    primary_stack.pop()
                    primary_stack_size -= 1
                    closing = True
                else:
                    # opening the node
                    visited.add(node.token["id"])
                    for child in node.children[::-1]:
                        primary_stack.append(child)
                        primary_stack_size += 1

                token = node.token
                print("closing: " if closing else "opening: ", token["form"])

                if not closing:
                    entity_stack_ptrs[token["id"]] = entity_stack_size
                    if token["upostag"] == "NOUN":
                        print(f"\tObject({token['lemma']})")
                        obj = Object(word=token["lemma"])
                        entity_stack.append(obj)
                        entity_stack_size += 1
                    if token["upostag"] == "ADP":
                        adp = Adposition.for_name(token["lemma"])
                        entity_stack[-2].make_relation(entity_stack[-1], adp)
                else:
                    ptr = entity_stack_ptrs[token["id"]]
                    frame = entity_stack[ptr:]
                    print(f"\tFrame: {frame}")
                    frame_size = entity_stack_size - ptr
                    if node is root:
                        scene.add_entities(*frame)
                        continue
                    if frame_size < 2:
                        continue

                    group = Group()
                    group.add_entities(*frame)

                    del entity_stack[ptr:]
                    entity_stack.append(group)
                    entity_stack_size -= frame_size - 1

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
