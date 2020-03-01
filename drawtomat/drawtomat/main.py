from drawtomat.language.udpipe_processor import UDPipeProcessor
import argparse

if __name__ == "main":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str)
    parser.add_argument("--output", default="../output/model.dot", type=str)
    args = parser.parse_args()

    processor = UDPipeProcessor("../resources/udpipe/english-ewt-ud-2.5-191206.udpipe")
    scene = processor.process(args.text)

    with open(args.output) as f:
        scene.export_dot(f)
