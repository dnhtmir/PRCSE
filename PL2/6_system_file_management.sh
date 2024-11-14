#!/bin/bash

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <directory> <size>"
    echo "Example: $0 /path/to/directory 100M"
    exit 1
fi

directory=$1
size=$2

if [[ ! -d "$directory" || ! -r "$directory" ]]; then
    echo "$directory is not readable or is not a directory."
    exit 1
fi

find "$directory" -type f -size +"$size" -print0 | while IFS= read -r -d '' file; do
    file_size=$(du -h "$file" | cut -f1)

    echo "File: $file (Size: $file_size)"
    echo "What would you like to do with this file?"
    echo "1) Delete"
    echo "2) Compress"
    echo "3) Skip"
    read -p "Enter your choice [1-3]: " choice

    case $choice in
        1)
            rm "$file"
            echo "File deleted."
            ;;
        2)
            gzip "$file"
            echo "File compressed."
            ;;
        3)
            echo "File skipped."
            ;;
        *)
            echo "Invalid choice. Skipping file."
            ;;
    esac
    echo
done