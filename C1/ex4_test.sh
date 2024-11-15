#!/bin/bash

# Make the script executable
script=./ex4.sh
chmod +x "$script"

# Function to verify the output
verify_output() {
    diff output.txt output2.txt > /dev/null
    if [ $? -ne 0 ]; then
        echo "Test $1 failed"
        echo "Expected output: $(cat output.txt)"
        echo "Actual output: $(cat output2.txt)"
    else
        echo "Test $1 passed"
    fi
    rm output.txt output2.txt
}

# Helper function to create files with specified number of lines
generate_file() {
    local file_name=$1
    local num_lines=$2
    > "$file_name"  # Create or clear the file

    for ((i = 1; i <= num_lines; i++)); do
        echo "line$i" >> "$file_name"
    done
    echo "File '$file_name' created with $num_lines lines."
}

# Function to create a test directory with sample files
create_test_dir() {
    local dir_name=$1
    mkdir -p "$dir_name"
    generate_file "$dir_name/file1.csv" 1
    generate_file "$dir_name/file2.csv" 2
    generate_file "$dir_name/file3.csv" 3
    generate_file "$dir_name/file4.csv" 4
    generate_file "$dir_name/file5.txt" 5
}

# Test 1: Wrong number of arguments
test_no=1
echo "Test $test_no: Feed wrong number of arguments"
$script 1 > output.txt
echo "Usage: $script <directory> <number of lines>" > output2.txt
verify_output $test_no

# Test 2: Extra argument provided
test_no=$((test_no + 1))
echo "Test $test_no: Feed wrong number of arguments"
$script 1 2 3 > output.txt
echo "Usage: $script <directory> <number of lines>" > output2.txt
verify_output $test_no

# Test 3: Non-existent folder
test_no=$((test_no + 1))
echo "Test $test_no: Feed non-existent folder"
$script ./non-existent 2 > output.txt
echo "Not a directory or you don't have reading permissions" > output2.txt
verify_output $test_no

# Test 4: File instead of directory
test_no=$((test_no + 1))
echo "Test $test_no: Feed file instead of folder"
file_name=./somefile.txt
touch "$file_name"
$script "$file_name" 2 > output.txt
echo "Not a directory or you don't have reading permissions" > output2.txt
verify_output $test_no
rm "$file_name"

# Test 5: Protected folder
test_no=$((test_no + 1))
echo "Test $test_no: Feed protected folder"
dir_name=./somedir
mkdir "$dir_name"
touch "$dir_name/$file_name"
chmod 000 "$dir_name"
$script "$dir_name" 2 > output.txt
echo "Not a directory or you don't have reading permissions" > output2.txt
verify_output $test_no
chmod 777 "$dir_name"
rm -rf "$dir_name"

# Test 6: Non-numeric second argument
test_no=$((test_no + 1))
echo "Test $test_no: Feed non-numeric value as second argument"
dir_name=./somedir
non_numeric_value="somestring"
mkdir "$dir_name"
$script "$dir_name" "$non_numeric_value" > output.txt
echo "$non_numeric_value is not an integer. Please insert an integer as the 2nd argument" > output2.txt
verify_output $test_no
rm -rf "$dir_name"

# Test 7: Zero as the second argument
test_no=$((test_no + 1))
echo "Test $test_no: Feed 0 as the second argument"
mkdir "$dir_name"
$script "$dir_name" 0 > output.txt
echo "Please provide a number larger than 0" > output2.txt
verify_output $test_no
rm -rf "$dir_name"

# Test 8: Negative number as the second argument
test_no=$((test_no + 1))
echo "Test $test_no: Feed negative number as the second argument"
mkdir "$dir_name"
$script "$dir_name" -3 > output.txt
echo "Please provide a number larger than 0" > output2.txt
verify_output $test_no
rm -rf "$dir_name"

# Test 9: Folder without CSV files
test_no=$((test_no + 1))
echo "Test $test_no: Folder without CSV files"
dir_name=./somedir
mkdir "$dir_name"
$script "$dir_name" 2 > output.txt
touch output2.txt
verify_output $test_no
rm -rf "$dir_name"

# Create artifacts for subsequent tests
echo ""
echo "Creating test files for the next tests..."
dir_name="./somedir"
create_test_dir $dir_name

# Test 10: Folder with mixed file types (n=2)
test_no=$((test_no + 1))
echo "Test $test_no: Folder with mixed file types (n=2)"
$script $dir_name 2 > output.txt
echo -e "$dir_name/file4.csv\n$dir_name/file3.csv" > output2.txt
verify_output $test_no

# Test 11: Folder with mixed file types (n=5)
test_no=$((test_no + 1))
echo "Test $test_no: Folder with mixed file types (n=5)"
$script $dir_name 5 > output.txt
echo -e "$dir_name/file4.csv\n$dir_name/file3.csv\n$dir_name/file2.csv\n$dir_name/file1.csv" > output2.txt
verify_output $test_no

# Clean up test artifacts
rm -rf $dir_name
