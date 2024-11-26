# Password Validator with Python
# a. Read a password as input.
# b. Verify if the password has between 8-16 characters.
# c. Consider a valid password if it contains lower case characters, upper case characters,
# numbers, and symbols.

import sys
import string
import getpass

def check_string_complexity(s):
    has_lower = any(char.islower() for char in s)
    has_upper = any(char.isupper() for char in s)
    has_digit = any(char.isdigit() for char in s)
    has_symbol = any(char in string.punctuation for char in s)
    return has_lower, has_upper, has_digit, has_symbol

if len(sys.argv) != 1:
    sys.exit("usage: " + sys.argv[0])

pw = ''
while not(8 <= len(pw) <= 16): # b)
    pw = getpass.getpass('password: ') # a) (invisible input)
    if not(8 <= len(pw) <= 16): # b)
        print('invalid pw')

if all(check_string_complexity(pw)):
    print('password is valid')
else:
    print('password is not valid')
