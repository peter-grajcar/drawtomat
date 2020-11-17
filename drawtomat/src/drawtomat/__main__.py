import argparse
import logging.config

from drawtomat.graphics import ConstraintComposer
from drawtomat.graphics.simple_renderer import SimpleRenderer
from drawtomat.language.udpipe_processor import UDPipeProcessor

# A dog and a chair are inside a house. The dog is sitting on the chair.

if __name__ == "__main__":
    logging.config.fileConfig(fname="resources/logging.conf", disable_existing_loggers=False)

    parser = argparse.ArgumentParser()
    parser.add_argument("--description", type=str)
    parser.add_argument("--model_output", default="output/model.dot", type=str)
    args = parser.parse_args()

    if not args.description:
        args.description = input("Description: ")

    processor = UDPipeProcessor("resources/udpipe/english-ewt-ud-2.5-191206.udpipe")
    scene = processor.process(args.description)

    graph = scene.export_dot(args.model_output)
    graph.graph_attr["label"] = f"\"{args.description}\""
    graph.graph_attr["labelloc"] = "t"
    graph.render(filename=args.model_output, format="png")

    composer = ConstraintComposer()
    entities = composer.compose(scene)

    renderer = SimpleRenderer(composer=composer, show_bounds=False)
    renderer.render(scene)
