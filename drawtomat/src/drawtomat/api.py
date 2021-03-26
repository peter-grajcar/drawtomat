import logging.config

import numpy as np
from flask import Flask, request

from drawtomat.composer import ConstraintComposer
from drawtomat.composer.factory import QuickDrawObjectFactory
from drawtomat.composer.scaler import AbsoluteObjectScaler, RelativeObjectScaler
from drawtomat.processor import UDPipeProcessor
from drawtomat.processor.word_embedding import WordEmbedding
from drawtomat.quickdraw import QuickDrawDataset

app = Flask(__name__)

logging.config.fileConfig(fname="resources/logging.conf", disable_existing_loggers=False)

processor = UDPipeProcessor("resources/udpipe/english-ewt-ud-2.5-191206.udpipe")
word_embedding = WordEmbedding(QuickDrawDataset.words())
obj_factory = QuickDrawObjectFactory(word_embedding)
obj_scaler_abs = AbsoluteObjectScaler(word_embedding)
obj_scaler_rel = RelativeObjectScaler(word_embedding)
composer = ConstraintComposer(obj_factory, obj_scaler_rel, use_ml=True)


@app.route("/drawtomat", methods=["POST"])
def drawtomat():
    desc = request.json["description"]
    scene = processor.process(desc)

    composer.use_ml = request.json["options"]["use_machine_learning"]
    composer.obj_scaler = obj_scaler_rel if request.json["options"]["use_relative_sizes"] else obj_scaler_abs

    entities = composer.compose(scene)
    drawing = [entity.get_relative_strokes() for entity in entities]
    extrema = [[min(stroke[0]), min(stroke[1]), max(stroke[0]), max(stroke[1])] for strokes in drawing for stroke in
               strokes]
    minima = np.min(extrema, axis=0)
    maxima = np.max(extrema, axis=0)
    return {
        "description": desc,
        "bounds": {
            "left": minima[0],
            "right": maxima[2],
            "bottom": minima[1],
            "top": maxima[3]
        },
        "drawing": drawing,
    }


@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Headers"] = "Content-Type"
    header["Access-Control-Allow-Origin"] = "*"
    return response
