#!/bin/bash

usage() {
    echo "usage: $(basename $0) <relationships.json> <objects.json>"
    exit 1
}

[ -z $1 -o -z $2 ] && usage

cat $1 | ./json2ndjson.sh | ./extract_relationships.py > "relationships.ndjson"
cat $2 | ./json2ndjson.sh | ./extract_objects.py > "objects.ndjson"

