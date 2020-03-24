import argparse

from drawtomat.graphics.quickdraw_renderer import QuickDrawRenderer
from drawtomat.language.udpipe_processor import UDPipeProcessor

if __name__ == "__main__":
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

    renderer = QuickDrawRenderer()
    renderer.render(scene)
