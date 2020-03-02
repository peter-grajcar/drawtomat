from drawtomat.language.adposition import Adposition
from drawtomat.language.udpipe_processor import UDPipeProcessor
import argparse

from drawtomat.model.object import Object
from drawtomat.model.scene import Scene

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str)
    parser.add_argument("--output", default="../output/model.dot", type=str)
    args = parser.parse_args()

    if not args.text:
        args.text = input()

    # processor = UDPipeProcessor("../resources/udpipe/english-ewt-ud-2.5-191206.udpipe")
    # scene = processor.process(args.text)

    scene = Scene()
    obj1 = Object(scene, "pencil")
    obj2 = Object(scene, "table")
    obj1.make_relation(obj2, Adposition.ON)

    with open(args.output, "w") as f:
        scene.export_dot(f)
