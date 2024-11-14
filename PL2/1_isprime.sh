#!/bin/bash

var=$1
var2=1

for (( i=1; i<=var-1; i++ ))
do
    # for the sake of speed and to avoid overflows: mod by value in every iteration
    var2=$((var2 * i % var))
done

if [[ $var2 -eq $((var - 1)) ]]
then
    echo "prime"
else
    echo "not prime"
fi
