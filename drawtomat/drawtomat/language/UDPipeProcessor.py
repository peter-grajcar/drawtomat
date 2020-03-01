from ufal.udpipe import Model, Pipeline, ProcessingError
from drawtomat.model.Scene import Scene


class UDPipeProcessor:
    """
    A description processor based on UDPipe.
    """
    model: Model

    def __init__(self, model_filename: str) -> None:
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
        pipeline = Pipeline(self.model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
        error = ProcessingError()
        processed = pipeline.process(text, error)

        # TODO: implement
