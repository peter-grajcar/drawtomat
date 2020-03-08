import argparse
from drawtomat.language.adposition import Adposition
from drawtomat.language.udpipe_processor import UDPipeProcessor
from drawtomat.model.group import Group
from drawtomat.model.object import Object
from drawtomat.model.scene import Scene

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
