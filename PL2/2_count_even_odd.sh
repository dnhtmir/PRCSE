#!/bin/bash

even_count=0
odd_count=0

for number in "$@"
do
    if (( number % 2 == 0 )); then
        ((even_count++))
    else
        ((odd_count++))
    fi
done

echo "Even count: $even_count"
echo "Odd count: $odd_count"
