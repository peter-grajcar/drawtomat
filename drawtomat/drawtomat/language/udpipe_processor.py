from collections import OrderedDict

import conllu
from conllu import TokenList
from ufal.udpipe import Model, Pipeline, ProcessingError

from drawtomat.language.adposition import Adposition
from drawtomat.model.group import Group
from drawtomat.model.object import Object
from drawtomat.model.scene import Scene


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

    def _process_adposition(self, sentence: 'TokenList', token) -> bool:
        """

        Parameters
        ----------
        sentence
        token

        Returns
        -------
        bool
            true if adposition should be skipped
        """
        token_idx = token["id"] - 1
        skip = False
        complex = None
        last = None

        # TODO: check length of the sentence
        # skips the beginning of complex adpositions
        # complex adposition of form PP, e.g. inside of
        if sentence[token_idx + 1]["upostag"] == "ADP":
            skip = True
            complex = token["form"] + " " + sentence[token_idx + 1]["form"]
            last = sentence[token_idx + 1]

        # complex adposition of form PNP, e.g. in front of
        if sentence[token_idx + 1]["upostag"] == "NOUN" and sentence[token_idx + 2]["upostag"] == "ADP":
            skip = True
            complex = token["form"] + " " + sentence[token_idx + 1]["form"] + " " + sentence[token_idx + 2]["form"]
            last = sentence[token_idx + 2]

        # complex adposition in form adverb/adjective + adposition, e.g. next to
        # (a complex adposition is formed only if it is in a list of adpositions)
        if sentence[token_idx - 1]["upostag"] == "ADV" or sentence[token_idx - 1]["upostag"] == "ADJ":
            complex = sentence[token_idx - 1]["form"] + " " + token["form"]
            if Adposition.for_name(complex):
                last = token
            else:
                complex = None

        if complex:
            if not last["misc"]:
                last["misc"] = OrderedDict()
            last["misc"]["Complex"] = complex

        return skip

    def _process_noun(self, sentence: 'TokenList', token) -> bool:
        token_idx = token["id"] - 1

        # TODO: check length
        # Noun is part of a complex adposition of form PNP
        if sentence[token_idx - 1]["upostag"] == "ADP" and sentence[token_idx + 1]["upostag"] == "ADP":
            return True
        # skip the first part of a compound noun
        if token["deprel"] == "compound":
            return True

        return False

    def _traverse_tree(self, parsed: 'list[TokenList]') -> Scene:
        """
        Processes the description via tree traversal (DFS).

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
                        skip = self._process_noun(sentence, token)

                        if not skip:
                            obj = None
                            obj_name = token["lemma"];
                            attrs = list()

                            for child in node.children:
                                # If a noun is preceded by 'the' try to find an existing object
                                # in scene's entity register.
                                if child.token["lemma"] == "the":
                                    for e in scene.entity_register:
                                        if type(e) == Object and e.word == token["lemma"]:
                                            obj = e
                                # extend the object name if the noun is a part of a compound noun
                                if child.token["deprel"] == "compound":
                                    obj_name = child.token["lemma"] + " " + obj_name
                                if child.token["upostag"] == "ADJ":
                                    attrs.append(child.token["lemma"])

                            if not obj:
                                obj = Object(scene, word=obj_name)
                                obj.attributes = attrs
                                print(f"\tnew Object({token['lemma']})")

                            entity_stack.append(obj)
                            entity_stack_size += 1
                            entity_position[obj] = token["id"]

                    # Creates relation between two objects at the top of
                    # the stack
                    if token["upostag"] == "ADP":
                        skip = self._process_adposition(sentence, token)

                        if not skip:
                            full_adp = token["form"]
                            if token["misc"] and token["misc"]["Complex"]:
                                full_adp = token["misc"]["Complex"]

                            print(f"\tnew Relation({full_adp})")
                            adp = Adposition.for_name(full_adp)

                            src =entity_stack[-2]
                            dst =entity_stack[-1]
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

        scene = self._traverse_tree(parsed)

        return scene
