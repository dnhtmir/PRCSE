#!/bin/bash

# check if the correct number of arguments is passed (2 arguments expected)
if [ $# -ne 2 ];
then
    echo "Usage: $0 <directory> <number of lines>"
    exit 1
fi

# check if the first argument is a readable directory
if [[ ! -r $1 || ! -d $1 ]];
then
    echo "Not a directory or you don't have reading permissions"
    exit 1
fi

# check if the second argument is a number
if ! [[ "$2" =~ ^-?[0-9]+$ ]];
then
    echo "$2 is not an integer. Please insert an integer as the 2nd argument"
    exit 1
fi

# check if the second argument is a positive number (greater than 0)
if [ "$2" -le 0 ];
then
    echo "Please provide a number larger than 0"
    exit 1
fi

# wc -l $1/*.csv -> returns a list of *.csv files under the specified directory
#                   along with their line count (-l) (and a summary line at the bottom)
#                   format: <number of lines> <file name>
# head -n -1 -> picks up the list that was returned by the previous command and removes
#               the last line (-n -1) (the summary line)
# sort -n -r -> sorts the list that was returned by the previous command by numerical
#               value (-n) in the reverse order (-r)
# head -n "$2" -> returns only the top "n" results (-n "$2") (number passed as the
#                 second argument) of the list that was returned by the previous command
# awk '{print $2}' -> since wc -l returned a result which was formatted like
#                     <number of lines> <file name>, and we only want the name of the file
#                     then this command picks up the output from the previous command
#                     and prints only <file name>
wc -l $1/*.csv | head -n -1 | sort -n -r | head -n "$2" | awk '{print $2}'
