#!/usr/bin/env python3
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str)
    parser.add_argument(
        "--path", default="/Volumes/SEAGATE M3/quickdraw-dataset", type=str
    )
    parser.add_argument("--count", default=100, type=int)
    args = parser.parse_args()

    print(args.name, file=sys.stderr)

    with open(f"{args.path}/{args.name}.ndjson") as f:
        for i in range(args.count):
            print(f.readline(), end="")
