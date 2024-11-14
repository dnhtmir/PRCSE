#!/bin/bash

declare -A group_info

while IFS=: read -r group_name _ gid _; do
    group_info["$gid"]="$group_name"
done < /etc/group

printf "%-10s %-20s\n" "GID" "Group Name"

for gid in "${!group_info[@]}"; do
    printf "%-10s %-20s\n" "$gid" "${group_info[$gid]}"
done
