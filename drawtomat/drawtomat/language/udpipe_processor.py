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
        dataset = QuickDrawDataset()
        pipeline = Pipeline(self.model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
        error = ProcessingError()
        processed = pipeline.process(text, error)
        parsed = conllu.parse(processed)

        print(processed)
        # print(parsed)

        scene = Scene()

        last_obj = None
        adp = None
        group = False

        for sentence in parsed:
            for token in sentence:
                if token["upostag"] == "NOUN":
                    unknown = False
                    if token["lemma"] in dataset.words:
                        print(f"object \"{token['lemma']}\"")
                    else:
                        print(f"unknown word: \"{token['form']}\"")
                        unknown = True

                    obj = Object(token["lemma"] + ("?" if unknown else ""), container=scene)

                    if last_obj and adp:
                        last_obj.make_relation(obj, adp)
                        adp = None
                    if last_obj and group:
                        g = Group(container=scene)
                        scene.entities.remove(last_obj)
                        scene.entities.remove(obj)
                        g.add_entities(last_obj, obj)
                        group = False

                        last_obj = g
                        continue

                    last_obj = obj

                elif token["upostag"] == "ADP":
                    adp = Adposition.for_name(token["lemma"])
                    print(f"relation {adp.name}") if adp else print(f"unsupported relation \"{token['form']}\"")
                elif token["lemma"] == "and":
                    group = True

        print(scene.entities)

        return scene
