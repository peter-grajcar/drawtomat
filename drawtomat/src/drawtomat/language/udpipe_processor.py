import logging
from collections import OrderedDict
from typing import List, Optional

import conllu
from conllu import TokenList
from ufal.udpipe import Model, Pipeline, ProcessingError

import drawtomat.language.text2num as t2n
from drawtomat.language.adposition import Adposition
from drawtomat.model.relational.group import Group
from drawtomat.model.relational.object import Object
from drawtomat.model.relational.scene import Scene


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
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.model:
            raise Exception(f"Cannot load model from file \"{model_filename}\".")

    def _process_adposition(self, sentence: 'TokenList', node) -> 'Optional[Adposition]':
        """

        Parameters
        ----------
        sentence : TokenList
            sentence as a list of tokens
        token

        Returns
        -------
        bool
            true if adposition should be skipped
        """
        token = node.token
        token_idx = token["id"] - 1
        skip = False
        complex_adp = None
        last = None

        prev_token = sentence[token_idx - 1] if token_idx > 0 else False
        next_token = sentence[token_idx + 1] if token_idx + 1 < len(sentence) else False
        next_next_token = sentence[token_idx + 2] if token_idx + 2 < len(sentence) else False

        # skips the beginning of complex adpositions
        # complex adposition of form PP, e.g. inside of
        if next_token and next_token["upostag"] == "ADP":
            skip = True
            complex_adp = token["form"] + " " + next_token["form"]
            last = next_token

        # complex adposition of form PNP, e.g. in front of
        if next_token and next_next_token and next_token["upostag"] == "NOUN" and next_next_token["upostag"] == "ADP":
            skip = True
            complex_adp = token["form"] + " " + next_token["form"] + " " + next_next_token["form"]
            last = next_next_token

        # complex adposition in form adverb/adjective + adposition, e.g. next to
        # (a complex adposition is formed only if it is in a list of adpositions)
        if prev_token and prev_token["upostag"] == "ADV" or prev_token["upostag"] == "ADJ":
            complex_adp = prev_token["form"] + " " + token["form"]
            if Adposition.for_name(complex_adp):
                last = token
            else:
                complex_adp = None

        if complex_adp:
            if not last["misc"]:
                last["misc"] = OrderedDict()
            last["misc"]["Complex"] = complex_adp

        if skip:
            return None

        full_adp = token["form"]
        if token["misc"] and token["misc"]["Complex"]:
            full_adp = token["misc"]["Complex"]

        self.logger.debug(f"\tnew Relation({full_adp})")

        return Adposition.for_name(full_adp)

    def _process_noun(self, scene: 'Scene', sentence: 'TokenList', node) -> 'Optional[Object]':
        token = node.token
        children = node.children
        token_idx = token["id"] - 1
        skip = False

        prev_token = sentence[token_idx - 1] if token_idx > 0 else False
        next_token = sentence[token_idx + 1] if token_idx + 1 < len(sentence) else False

        # Noun is part of a complex adposition of form PNP
        if prev_token and next_token and prev_token["upostag"] == "ADP" and next_token["upostag"] == "ADP":
            skip = True
        # skip the first part of a compound noun
        if token["deprel"] == "compound":
            skip = True

        if skip:
            return None

        count = 1
        obj = None
        obj_name = token["lemma"]
        attrs = list()

        for child in children:
            # If a noun is preceded by 'the' try to find an existing object
            # in scene's entity register.
            if child.token["lemma"] == "the":
                for e in reversed(list(scene.entity_register)):
                    if type(e) == Object and e.word == token["lemma"]:
                        obj = e
            # extend the object name if the noun is a part of a compound noun
            if child.token["deprel"] == "compound":
                obj_name = child.token["lemma"] + " " + obj_name
            if child.token["upostag"] == "ADJ":
                attrs.append(child.token["lemma"])
            if child.token["upostag"] == "NUM":
                count = int(child.token["lemma"])

        if not obj:
            if count == 1:
                obj = Object(scene, word=obj_name)
                obj.attributes = attrs

                self.logger.debug(f"\tnew Object({token['lemma']})")
            else:
                count = max(count, 10)  # TODO: add MAX_COUNT
                obj = Group(scene)
                for _ in range(count):
                    obj.add_entity(Object(scene, word=obj_name, attrs=attrs))

                self.logger.debug(f"new Group({count}x{obj_name})")

        return obj

    def _traverse_tree(self, parsed: 'List[TokenList]') -> 'Scene':
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

                self.logger.debug(f"{'closing' if closing else 'opening'}: {token['form']}")

                if not closing:
                    entity_stack_ptrs[token["id"]] = entity_stack_size

                    if token["upostag"] == "NOUN" or token["upostag"] == "PROPN":
                        obj = self._process_noun(scene, sentence, node)

                        if obj:
                            entity_stack.append(obj)
                            entity_stack_size += 1
                            entity_position[obj] = token["id"]

                    # Creates relation between two objects at the top of
                    # the stack
                    if token["upostag"] == "ADP":
                        adp = self._process_adposition(sentence, node)

                        if adp:
                            src = entity_stack[-2]
                            dst = entity_stack[-1]
                            if entity_position[src] > entity_position[dst]:
                                src, dst = dst, src

                            src.make_relation(dst, adp)
                # closing the node
                else:
                    ptr = entity_stack_ptrs[token["id"]]
                    frame = entity_stack[ptr:]
                    frame_size = entity_stack_size - ptr
                    self.logger.debug(f"\tFrame:\t{frame}")

                    frame_set = set()
                    frame_set_size = 0
                    for e in frame:
                        if e.container is None:
                            frame_set.add(e)
                            frame_set_size += 1

                    # if there are at least two entities in the entity stack frame
                    # merge them into one group.
                    if frame_set_size > 1:
                        self.logger.debug(f"\tnew Group({frame_set_size})")

                        g = Group(scene, entities=frame_set)
                        entity_position[g] = max([entity_position[e] for e in frame])

                        del entity_stack[ptr:]
                        entity_stack.append(g)
                        entity_stack_size -= frame_size - 1

            # Put all entities which does not belong to any group to the scene
            for e in entity_stack:
                if e.container is None:
                    scene.add_entity(e)

            self.logger.debug("done")

        return scene

    def _preprocess(self, text: 'str') -> 'str':
        text_preprocessed = t2n.replace_with_numbers(text)
        self.logger.debug(f"preprocessed input: {text_preprocessed}")
        return text_preprocessed

    def process(self, text: 'str') -> 'Scene':
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
        text_preprocessed = self._preprocess(text)

        pipeline = Pipeline(self.model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
        error = ProcessingError()
        processed = pipeline.process(text_preprocessed, error)
        parsed = conllu.parse(processed)

        scene = self._traverse_tree(parsed)

        return scene
