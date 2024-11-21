#!/bin/bash
# ============================================================
# Name: PG_SICP_PRCSE_Group4_C1_Ex3_test.sh
# Description: Validate the functionality of script PG_SICP_PRCSE_Group4_C1_Ex3.sh
# Author: Group 4
# Created On: 2024-11-15
# Last Modified: 2024-11-15
# Usage: ./PG_SICP_PRCSE_Group4_C1_Ex3_test.sh
# ============================================================

#Temp folder for test if needed
readonly TEMP_FOLDER="PG_SICP_PRCSE_Group4_C1_Ex3_test_TEMP"

#global variables to count test results
n_succeeded=0
n_failed=0

#print test status
status()
{
    exit_status=$1
    expected_status=$2

    if [ "$exit_status" -ne "$expected_status" ]; then
        echo -e "\033[0;31mTest failed\033[0m\n"
        ((n_failed++))
    else
        echo -e "\033[0;32mTest succeeded\033[0m\n"
        ((n_succeeded++))
    fi
}

#get exit value from sh execution
check_exit_status()
{
    exit_status=$?

    expected_status=$1

    status $exit_status $expected_status
}

#force status and print the result
force_status()
{
    if [ $1 -eq 1 ]; then
        status 1 1
    else
        status 1 0
    fi

}

#Test 1------------------------------------------------------------------------------
echo -e "\n----------------- Test 1: Incorrect number of parameters -----------------"
./PG_SICP_PRCSE_Group4_C1_Ex3.sh "param1" "param2" "param3"
check_exit_status 1

#Test 2------------------------------------------------------------------------------
echo -e "\n----------------- Test 2: Is not a directory -----------------"
./PG_SICP_PRCSE_Group4_C1_Ex3.sh "thisisnotadirectory"
check_exit_status 1

#Test 3------------------------------------------------------------------------------
echo -e "\n----------------- Test 3: Correct Execution -----------------"

echo "Test 3 setup..."

#create directory
echo "Temp folder is:" $TEMP_FOLDER
mkdir $TEMP_FOLDER
cd $TEMP_FOLDER

#create 5 files
touch file1.txt
touch file2.txt
touch file3.txt
touch file4.txt
touch file5.txt

#create 2 groups
sudo groupadd tempgroup1
sudo groupadd tempgroup2

#associate 2 groups to files
sudo chgrp tempgroup1 file1.txt
sudo chgrp tempgroup1 file2.txt
sudo chgrp tempgroup2 file3.txt
sudo chgrp tempgroup1 file4.txt
sudo chgrp tempgroup2 file5.txt

#give g+r to 3 files and remove for the others
chmod g+r file1.txt
chmod g+r file2.txt
chmod g+r file3.txt
chmod g-r file4.txt
chmod g-r file5.txt

#folder ls
ls -l

#1 level back
cd ..

echo -e "\nScript result:"

#execute script
output=$(./PG_SICP_PRCSE_Group4_C1_Ex3.sh "$TEMP_FOLDER")

#print script output
printf "%s\n" "$output"

#count output lines
n_lines=$(printf "%s\n" "$output" | wc -l)


if [ "$n_lines" -eq 3 ]; then
    #if 3 lines - OK
    
    if [[ "$output" == *"file1"* && "$output" == *"file2"* && "$output" == *"file3"* ]]; then
        #contains file1,file2,file3 - OK
        check_exit_status 0
    else
        #didn't detect the 3 files -NOK
        echo -e "\nIncorrect files detected\n" 
        force_status 0
    fi
else
    #detected more than 3 - NOK
    printf "\n#lines %d != 3\n" $n_lines
    force_status 0
fi

#clean test

#delete directory and files
rm -r $TEMP_FOLDER

#delete groups
sudo groupdel tempgroup1
sudo groupdel tempgroup2

#Summary
printf "\n----------------- SUMMARY -----------------\nFailed:\033[0;31m%d\033[0m \nSucceeded:\033[0;32m%d\033[0m\n" $n_failed $n_succeeded 
