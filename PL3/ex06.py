# Guessing Game with Python
# a. Generate a random number at the beginning of the game.
# b. Tell the user if the number he guessed is lower, higher, or equal to the generated number
# (stop the game when he is right).
# c. Track the total number of user guesses and display this information at the end of the
# game.
# d. Ask if the user wants to play again (or leave) and, if so, re-start the game.

import random
import sys
    

if len(sys.argv) != 1:
    sys.exit("usage: " + sys.argv[0])

lower_limit = 1
upper_limit = 10

keep_going_query = 'y'
while keep_going_query == 'y':
    # a)
    random_number = random.randint(lower_limit, upper_limit)
    total_attempts = 0

    # b)
    attempt = -1
    while attempt != random_number:
        attempt = int(input('insert a number from ' + str(lower_limit) + ' to ' + str(upper_limit) + ': '))
        if not (lower_limit <= attempt <= upper_limit):
            print('value must be between ' + str(lower_limit) + ' and ' + str(upper_limit))
            continue

        total_attempts += 1 # c)
        if attempt > random_number:
            print(str(attempt) + ' is greater than the random number')
        elif attempt < random_number:
            print(str(attempt) + ' is smaller than the random number')
    
    print(str(attempt) + ' is equal to the random number: ' + str(random_number))
    print('you won!')

    # c)
    print('total attempts: ' + str(total_attempts))

    # d)
    while True:
        keep_going_query = input('do you want to keep going? (y/n)')
        if keep_going_query != 'y' and keep_going_query != 'n':
            print('invalid input, please insert "y" or "n": ')
            continue
        break
