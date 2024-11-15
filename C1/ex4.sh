#!/bin/bash

if [ $# -ne 2 ];
then
    echo "Usage: $0 <directory> <number of lines>"
    exit 1
fi

if [[ ! -r $1 || ! -d $1 ]];
then
    echo "Not a directory or you don't have reading permissions"
    exit 1
fi

if ! [[ "$2" =~ ^-?[0-9]+$ ]]; then
    echo "$2 is not an integer. Please insert an integer as the 2nd argument"
    exit 1
fi

if [ "$2" -le 0 ]; then
    echo "Please provide a number larger than 0"
    exit 1
fi

wc -l $1/*.csv | head -n -1 | sort -n -r | head -n "$2" | awk '{print $2}'
