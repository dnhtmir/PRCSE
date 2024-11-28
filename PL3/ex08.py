# Password Generator with Python
# a. When requested generate a random password with python.
# b. The password must be valid according to your python password validator (exercise 7).

import random
import sys
import string

def generate_password(min_len, max_len):
    if min_len > max_len:
        raise ValueError("min_len should not be greater than max_len.")
    
    length = random.randint(min_len, max_len)
    
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string

def check_string_complexity(s):
    has_lower = any(char.islower() for char in s)
    has_upper = any(char.isupper() for char in s)
    has_digit = any(char.isdigit() for char in s)
    has_symbol = any(char in string.punctuation for char in s)
    return has_lower, has_upper, has_digit, has_symbol

if len(sys.argv) != 1:
    sys.exit("usage: " + sys.argv[0])

pw = ''
attempts = 0
while True: # infinite loop
    attempts += 1
    pw = generate_password(8, 16) # a)
    if all(check_string_complexity(pw)) and 8 <= len(pw) <= 16: # b)
        break

print('after ' + str(attempts) + ' attempts')
print("here's your password: " + pw)
