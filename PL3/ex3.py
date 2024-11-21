# Write a script that receives a word as argument and verifies if it is a palindrome. A palindrome
# is a sequence of characters which reads the same backward as forward, such as madam or
# racecar.

import sys

if len(sys.argv) != 2:
    sys.exit("usage: " + sys.argv[0] + " <string>")
    
str_to_test = sys.argv[1]

if str_to_test == str_to_test[::-1]:
    print("is palindrome")
else:
    print("isn't palindrome")
