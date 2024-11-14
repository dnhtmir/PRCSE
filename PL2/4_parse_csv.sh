#!/bin/bash

if [[ -z $1 ]]; then
    echo "Please provide a .csv file."
    exit 1
fi

if [[ ! -f $1 || ${1: -4} != ".csv" ]]; then
    echo "The provided file is not a valid .csv file."
    exit 1
fi

min_salary=999999
max_salary=0
min_age=999
max_age=0
total_salary=0
total_age=0
salary_count=0
age_count=0
declare -A age_salary_map

while IFS=, read -r name age salary; do
    if [[ "$name" == "Name" ]]; then
        continue
    fi
    
    if (( salary < min_salary )); then
        min_salary=$salary
        min_salary_name=$name
    fi
    
    if (( salary > max_salary )); then
        max_salary=$salary
        max_salary_name=$name
    fi
    
    if (( age < min_age )); then
        min_age=$age
        min_age_name=$name
    fi
    
    if (( age > max_age )); then
        max_age=$age
        max_age_name=$name
    fi

    total_salary=$((total_salary + salary))
    total_age=$((total_age + age))
    ((salary_count++))
    ((age_count++))

    age_salary_map[$age]+="$salary "
done < "$1"

average_salary=$(echo "$total_salary / $salary_count" | bc -l)
average_age=$(echo "$total_age / $age_count" | bc -l)

calculate_median() {
    local arr=($(echo "$1" | tr ' ' '\n' | sort -n))
    local count=${#arr[@]}
    if (( count % 2 == 1 )); then
        echo "${arr[$((count / 2))]}"
    else
        local mid=$((count / 2))
        echo "scale=2; (${arr[$mid-1]} + ${arr[$mid]}) / 2" | bc
    fi
}

echo "Minimum Salary: $min_salary (Employee: $min_salary_name)"
echo "Maximum Salary: $max_salary (Employee: $max_salary_name)"
echo "Minimum Age: $min_age (Employee: $min_age_name)"
echo "Maximum Age: $max_age (Employee: $max_age_name)"
echo "Average Salary: $(printf "%.2f" $average_salary)"
echo "Average Age: $(printf "%.2f" $average_age)"
echo "Median Salary by Age:"

for age in "${!age_salary_map[@]}"; do
    median_salary=$(calculate_median "${age_salary_map[$age]}")
    echo -e "Age $age:\t$median_salary"
done