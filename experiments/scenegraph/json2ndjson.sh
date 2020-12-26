#!/bin/bash

usage() {
    echo "usage: $(basename $0) <input file> <output file>"
    exit 1
}

[ -z $1 ] && usage

cat $1 | jq -c '.[]'

