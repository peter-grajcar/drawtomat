import argparse

from drawtomat.graphics.quickdraw_composer import QuickDrawComposer
from drawtomat.language.udpipe_processor import UDPipeProcessor

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str)
    parser.add_argument("--output", default="../output/model.dot", type=str)
    args = parser.parse_args()

    if not args.text:
        args.text = input()

    processor = UDPipeProcessor("../resources/udpipe/english-ewt-ud-2.5-191206.udpipe")
    scene = processor.process(args.text)

    graph = scene.export_dot(args.output)
    graph.graph_attr["label"] = f"\"{args.text}\""
    graph.graph_attr["labelloc"] = "t"
    graph.view()

    composer = QuickDrawComposer()
    composer.compose(scene)
