#!/bin/bash

script=./ex4.sh
chmod +x $script

verify_output() {
    # Compare the actual output with the expected output
    diff output.txt output2.txt > /dev/null

    # Check if diff found any differences
    if [ $? -ne 0 ]; then
        echo "Test $1 failed"
        echo "expected output $(cat output.txt)"
        echo "actual output $(cat output2.txt)"
    else
        echo "Test $1 passed"
    fi

    rm output.txt output2.txt
}

test_no=1
echo "Test $test_no: Feed wrong number of arguments"
$script 1 > output.txt
echo "Usage: $script <directory> <number of lines>" > output2.txt
verify_output $test_no

test_no=$((test_no+1))
echo "Test $test_no: Feed wrong number of arguments"
$script 1 2 3 > output.txt
echo "Usage: $script <directory> <number of lines>" > output2.txt
verify_output $test_no

test_no=$((test_no+1))
echo "Test $test_no: Feed non-existent folder"
$script ./non-existent 2 > output.txt
echo "Not a directory or you don't have reading permissions" > output2.txt
verify_output $test_no

test_no=$((test_no+1))
echo "Test $test_no: Feed file instead of folder"
file_name=./somefile.txt
touch $file_name # test file creation
$script $file_name 2 > output.txt
echo "Not a directory or you don't have reading permissions" > output2.txt
verify_output $test_no
rm $file_name # delete test file

test_no=$((test_no+1))
echo "Test $test_no: Feed protected folder"
dir_name=./somedir
mkdir $dir_name # test folder creation
touch $dir_name/$file_name # creation of a file inside the folder 
chmod 000 $dir_name # remove all permissions from the folder
$script $dir_name 2 > output.txt
echo "Not a directory or you don't have reading permissions" > output2.txt
verify_output $test_no
chmod 777 $dir_name # re-assign all permissions to the folder (so it can be removed)
rm -rf $dir_name # delete test folder (and its contents)

test_no=$((test_no+1))
echo "Test $test_no: Feed non-numeric value as the second argument"
dir_name=./somedir
non_numeric_value=somestring
mkdir $dir_name # test folder creation
$script $dir_name $non_numeric_value > output.txt
echo "$non_numeric_value is not an integer. Please insert an integer as the 2nd argument" > output2.txt
verify_output $test_no
rm -rf $dir_name # delete test folder (and its contents)

test_no=$((test_no+1))
echo "Test $test_no: Feed 0 as the second argument"
dir_name=./somedir
mkdir $dir_name # test folder creation
$script $dir_name 0 > output.txt
echo "Please provide a number larger than 0" > output2.txt
verify_output $test_no
rm -rf $dir_name # delete test folder (and its contents)

test_no=$((test_no+1))
echo "Test $test_no: Feed negative number as the second argument"
dir_name=./somedir
mkdir $dir_name # test folder creation
$script $dir_name -3 > output.txt
echo "Please provide a number larger than 0" > output2.txt
verify_output $test_no
rm -rf $dir_name # delete test folder (and its contents)

test_no=$((test_no+1))
echo "Test $test_no: Folder without csv files"
dir_name=./somedir
mkdir $dir_name # test folder creation
$script $dir_name 2 > output.txt
touch output2.txt
verify_output $test_no
rm -rf $dir_name # delete test folder (and its contents)

# fixture for next tests
echo ""
echo "Creation of artifacts for the next tests"

generate_file() {
    for ((i = 1; i <= 2; i++)); do
        echo "line$i" >> "$1"
    done

    echo "File '$1' created with $2 lines."
}

dir_name=./somedir
mkdir $dir_name # test folder creation
generate_file $dir_name/file1.csv 1
generate_file $dir_name/file2.csv 2
generate_file $dir_name/file3.csv 3
generate_file $dir_name/file4.csv 4
generate_file $dir_name/file5.txt 5

test_no=$((test_no+1))
echo "Test $test_no: Folder with multiple types of files (n=2)"
$script $dir_name 2 > output.txt
echo -e "$dir_name/file4.csv\n$dir_name/file3.csv" > output2.txt
verify_output $test_no

test_no=$((test_no+1))
echo "Test $test_no: Folder with multiple types of files (n=5)"
$script $dir_name 5 > output.txt
echo -e "$dir_name/file4.csv\n$dir_name/file3.csv\n$dir_name/file2.csv\n$dir_name/file1.csv" > output2.txt
verify_output $test_no

rm -rf $dir_name # delete test folder (and its contents)

