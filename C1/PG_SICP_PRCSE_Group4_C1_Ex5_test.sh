#!/bin/bash
# ============================================================
# Name: PG_SICP_PRCSE_Group4_C1_Ex5_test.sh
# Description: Validate the functionality of script PG_SICP_PRCSE_Group4_C1_Ex5.sh
# Author: Group 4
# Created On: 2024-11-16
# Last Modified: 2024-11-16
# Usage: sudo ./PG_SICP_PRCSE_Group4_C1_Ex5_test.sh 
# ============================================================

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
echo -e "\n----------------- Test 1: Basic Exection (guarantee permissions etc)  -----------------"
./PG_SICP_PRCSE_Group4_C1_Ex5.sh
check_exit_status 0

#Test 2------------------------------------------------------------------------------
echo -e "\n----------------- Test 2: 3 users with pwd exp., 1 without  -----------------"

echo "Create group:"

#create temp group
sudo groupadd group_temp_ex5
getent group group_temp_ex5

#create users with expiration date in the following 3 days
echo -e "\n"
sudo useradd -g group_temp_ex5 user0_temp_ex5 
echo "user0_temp_ex5:palavra_passe" | sudo chpasswd
sudo chage -M 0 user0_temp_ex5 #today
id user0_temp_ex5
sudo chage -l user0_temp_ex5


echo -e "\n"
sudo useradd -g group_temp_ex5 user1_temp_ex5 
echo "user1_temp_ex5:palavra_passe" | sudo chpasswd
sudo chage -M 1 user1_temp_ex5 #today+1
id user1_temp_ex5
sudo chage -l user1_temp_ex5

echo -e "\n"
sudo useradd -g group_temp_ex5 user2_temp_ex5 
echo "user2_temp_ex5:palavra_passe" | sudo chpasswd
sudo chage -M 2 user2_temp_ex5 #today+2
id user2_temp_ex5
sudo chage -l user2_temp_ex5

echo -e "\n"
sudo useradd -g group_temp_ex5 user3_temp_ex5 
echo "user3_temp_ex5:palavra_passe" | sudo chpasswd
sudo chage -M 3 user3_temp_ex5 #today+3
id user3_temp_ex5
sudo chage -l user3_temp_ex5


#create a user with expiration date in the following 4 days
echo -e "\n"
sudo useradd -g group_temp_ex5 user4_temp_ex5 
echo "user4_temp_ex5:palavra_passe" | sudo chpasswd
sudo chage -M 4 user4_temp_ex5 #today+4
id user4_temp_ex5
sudo chage -l user4_temp_ex5


echo -e "\nexecute..."
output=$(./PG_SICP_PRCSE_Group4_C1_Ex5.sh)

printf "%s\n" "$output"

if [[ "$output" == *"user0_temp_ex5"* && "$output" == *"user1_temp_ex5"* && "$output" == *"user2_temp_ex5"* && "$output" == *"user3_temp_ex5"* && "$output" != *"user4_temp_ex5"* ]]; then
    #contains user0_temp_ex5, user1_temp_ex5,user2_temp_ex5,user3_temp_ex5 and !user4_temp_ex5 - OK
    check_exit_status 0
else
    #NOK
    echo "users didn't find" 
    force_status 0
fi

echo "clean test data..."
#clean test data
sudo userdel user0_temp_ex5 
sudo userdel user1_temp_ex5 
sudo userdel user2_temp_ex5 
sudo userdel user3_temp_ex5 
sudo userdel user4_temp_ex5 
sudo groupdel group_temp_ex5


#Summary
printf "\n----------------- SUMMARY -----------------\nFailed:\033[0;31m%d\033[0m \nSucceeded:\033[0;32m%d\033[0m\n" $n_failed $n_succeeded 