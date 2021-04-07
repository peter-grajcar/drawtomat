import argparse
import logging.config

from drawtomat.composer import ConstraintComposer
from drawtomat.composer.factory.quickdraw_object_factory import QuickDrawObjectFactory
from drawtomat.composer.scaler.absolute_object_scaler import AbsoluteObjectScaler
from drawtomat.processor.udpipe_processor import UDPipeProcessor
# A dog and a chair are inside a house. The dog is sitting on the chair.
from drawtomat.processor.word_embedding import WordEmbedding
from drawtomat.quickdraw import QuickDrawDataset
from drawtomat.renderer.simple_renderer import SimpleRenderer

if __name__ == "__main__":
    logging.config.fileConfig(fname="resources/logging.conf", disable_existing_loggers=False)

    parser = argparse.ArgumentParser()
    parser.add_argument("--description", type=str)
    parser.add_argument("--graph_output", type=str)
    parser.add_argument("--image_output", default="drawing.png", type=str)
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    if not args.description:
        args.description = input("Description: ")

    processor = UDPipeProcessor("resources/udpipe/english-ewt-ud-2.5-191206.udpipe")
    scene = processor.process(args.description)

    if args.graph_output:
        graph = scene.export_dot(args.graph_output)
        graph.graph_attr["label"] = f"\"{args.description}\""
        graph.graph_attr["labelloc"] = "t"
        graph.render(filename=args.graph_output, format="png")

    word_embedding = WordEmbedding(QuickDrawDataset.words())
    obj_factory = QuickDrawObjectFactory(word_embedding)
    obj_scaler = AbsoluteObjectScaler(word_embedding)
    composer = ConstraintComposer(obj_factory, obj_scaler)
    entities = composer.compose(scene)

    renderer = SimpleRenderer(composer=composer, show_bounds=False)
    renderer.render(scene, show=args.show, output=args.image_output)
