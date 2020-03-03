from drawtomat.language.adposition import Adposition
from drawtomat.language.udpipe_processor import UDPipeProcessor
import argparse

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

    # processor = UDPipeProcessor("../resources/udpipe/english-ewt-ud-2.5-191206.udpipe")
    # scene = processor.process(args.text)

    scene = Scene()

    grp1 = Group(scene)
    obj1 = Object(grp1, "pencil")
    obj2 = Object(grp1, "book")
    obj3 = Object(scene, "table")
    obj4 = Object(scene, "cat")

    grp1.make_relation(obj3, Adposition.ON)
    obj4.make_relation(obj3, Adposition.UNDER)

    with open(args.output, "w") as f:
        scene.export_dot(f)
