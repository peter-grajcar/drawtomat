import logging.config

import numpy as np
from flask import Flask, request

from drawtomat.graphics import ConstraintComposer
from drawtomat.language import UDPipeProcessor
from drawtomat.quickdraw.quickdraw_object_factory import QuickDrawObjectFactory

app = Flask(__name__)

logging.config.fileConfig(fname="resources/logging.conf", disable_existing_loggers=False)

processor = UDPipeProcessor("resources/udpipe/english-ewt-ud-2.5-191206.udpipe")
obj_factory = QuickDrawObjectFactory()
composer = ConstraintComposer(obj_factory)


@app.route("/drawtomat", methods=["POST"])
def drawtomat():
    desc = request.json["description"]
    scene = processor.process(desc)

    entities = composer.compose(scene)
    drawing = [entity.get_relative_strokes() for entity in entities]
    extrema = [[min(stroke[0]), min(stroke[1]), max(stroke[0]), max(stroke[1])] for strokes in drawing for stroke in strokes]
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
