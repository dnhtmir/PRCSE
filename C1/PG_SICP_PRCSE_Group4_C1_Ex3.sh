#!/bin/bash
# ============================================================
# Name: PG_SICP_PRCSE_Group4_C1_Ex3.sh
# Description: Outputs to the screen all files in a given directory that have read permissions for the group. The directory is provided as a parameter.
# Author: Group 4
# Created On: 2024-11-15
# Last Modified: 2024-11-15
# Usage: ./PG_SICP_PRCSE_Group4_C1_Ex3.sh [directory]
# ============================================================

readonly MAX_PARAMETERS=1

#only accept 1 parameter
if ! [ $# -eq $MAX_PARAMETERS ]; then
    printf "[ERROR] received %d parameters, only 1 parameter (the directory) is accepted.\n" $# >&2
    exit 1
fi

#is it a directory?
directory=$1

if ! [[ -d "$directory" ]]; then
    printf "[ERROR] %s is not a directory.\n" $directory >&2
    exit 1
fi

#type: file
#perm: only files with group read permission

#exec: A find command option that allows you to execute an external command (in this case, ls -l) on each item found. *AFTER THE FILTER*
#      ls -l: Displays detailed information about a file, such as permissions, owner, group, size, and last modification date.
#      {}: A placeholder replaced by the full path of each file or directory found by the find command.
#      \;: Indicates the end of the command to execute. The backslash (\) escapes the semicolon (;) so it is interpreted correctly by the shell.

#awk: filter the output to print the file and group
find $directory -type f -perm /g+r -exec ls -l {} \; | awk '{printf "  > file:%s, group:%s\n",$9,$4}'

exit 0
