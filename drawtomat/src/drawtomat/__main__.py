import argparse
import logging.config

from drawtomat.composer import ConstraintComposer
from drawtomat.composer.factory.quickdraw_object_factory import QuickDrawObjectFactory
from drawtomat.composer.scaler import AbsoluteObjectScaler, RelativeObjectScaler
from drawtomat.processor.udpipe_processor import UDPipeProcessor
# A dog and a chair are inside a house. The dog is sitting on the chair.
from drawtomat.processor.word_embedding import WordEmbedding
from drawtomat.quickdraw import QuickDrawDataset
from drawtomat.renderer.simple_renderer import SimpleRenderer

if __name__ == "__main__":
    logging.config.fileConfig(fname="resources/logging.conf", disable_existing_loggers=False)

    parser = argparse.ArgumentParser()
    parser.add_argument("--description", type=str, help="Specifies the image description. If not set the description "
                                                        "is taken from the standard input.")
    parser.add_argument("--graph_output", type=str, help="Scene graph output path.")
    parser.add_argument("--sizes", type=str, choices=["absolute", "relative"], default="absolute", help="Approach for determining the object size. Default is 'absolute'.")
    parser.add_argument("--constraints", type=str, choices=["rule", "classifier"], default="rule", help="Type of the constraints. Default is 'rule'.")
    parser.add_argument("--image_output", default="drawing.png", type=str, help="Image output path. Default is "
                                                                                "drawing.png")
    parser.add_argument("--show", action="store_true", default="Show the image after it is generated.")
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

    if args.sizes == "absolute":
        obj_scaler = AbsoluteObjectScaler(word_embedding)
    elif args.sizes == "relative":
        obj_scaler = RelativeObjectScaler(word_embedding)
    else:
        raise ValueError(f"Invalid scaler type '{args.sizes}'.")

    composer = ConstraintComposer(obj_factory, obj_scaler, constraints=args.constraints)
    entities = composer.compose(scene)
    renderer = SimpleRenderer(composer=composer, show_bounds=False)
    renderer.render(scene, show=args.show, output=args.image_output)
