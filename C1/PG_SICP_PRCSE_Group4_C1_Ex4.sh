#!/bin/bash
# ============================================================
# Name: PG_SICP_PRCSE_Group4_C1_Ex4.sh
# Description: Outputs to the screen 'n' *.csv files in a given directory with the highest line count.
# Author: Group 4
# Created On: 2024-11-17
# Last Modified: 2024-11-17
# Usage: ./PG_SICP_PRCSE_Group4_C1_Ex4.sh [directory] [numberfiles]
# ============================================================

# check if the correct number of arguments is passed (2 arguments expected)
if [ $# -ne 2 ];
then
    echo "Usage: $0 <directory> <number of lines>"
    exit 1
fi

target_dir=$1
number_files=$2

# check if the first argument is a readable directory
if [[ ! -r $target_dir || ! -d $target_dir ]];
then
    echo "Not a directory or you don't have reading permissions"
    exit 1
fi

# check if the second argument is a number
if ! [[ "$number_files" =~ ^-?[0-9]+$ ]];
then
    echo "$number_files is not an integer. Please insert an integer as the 2nd argument"
    exit 1
fi

# check if the second argument is a positive number (greater than 0)
if [ "$number_files" -le 0 ];
then
    echo "Please provide a number larger than 0"
    exit 1
fi

# wc -l $target_dir/*.csv -> returns a list of *.csv files under the specified directory
#                            along with their line count (-l) (and a summary line at the bottom)
#                            format: <number of lines> <file name>
#              head -n -1 -> picks up the list that was returned by the previous command and removes
#                            the last line (-n -1) (the summary line)
#              sort -n -r -> sorts the list that was returned by the previous command by numerical
#                            value (-n) in the reverse order (-r)
# head -n "$number_files" -> returns only the top "n" results (-n "$number_files")
#                            (number passed as the second argument) of the list that was
#                            returned by the previous command
#        awk '{print $2}' -> since wc -l returned a result which was formatted like
#                            <number of lines> <file name>, and we only want the name of the file
#                            then this command picks up the output from the previous command
#                            and prints only <file name>
wc -l $target_dir/*.csv | head -n -1 | sort -n -r | head -n "$number_files" | awk '{print $2}'
