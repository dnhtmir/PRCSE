#!/bin/bash

if [[ -z $1 ]]; then
    echo "Please provide a directory."
    exit 1
fi

if [[ ! -d $1 ]]; then
    echo "The provided argument is not a directory."
    exit 1
fi

if [[ ! -r $1 ]]; then
    echo "The provided directory is not readable."
fi

for file in "$1"/*.txt; do
    if [[ -f $file ]]; then
        head -n 1 "$file"
    fi
done
