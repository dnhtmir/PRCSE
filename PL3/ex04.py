# Ask the user to provide an array of numbers (integers or floats, positive or negative) with
# variable length. For the given array compute:
# a. Mean
# b. Median
# c. Max, Minimum
# d. Variance
# e. Standard Deviation
# f. Number of positive and negative numbers

import sys
import math

if len(sys.argv) <= 1:
    sys.exit("usage: " + sys.argv[0] + " <values>")

array = []
max = 50
total = 0
count_pos = 0
count_neg = 0
for n in sys.argv[1:]:
    val = float(n)
    array.append(val)
    if val > 0:
        count_pos += 1
    if val < 0:
        count_neg -= 1

# calc mean
mean = sum(array) / len(array)

# calc median
array.sort()
if len(array) % 2 == 0:
    a = len(array) / 2 - 1
    b = len(array) / 2
    median = (array[int(a)] + array[int(b)]) / 2
else:
    a = (len(array) - 1) / 2
    median = array[int(a)]

# calc max and min
max = array[-1]
min = array[0]

# calc variance and standard deviation
variance = sum((x - mean) ** 2 for x in array) / len(array)
std_dev = math.sqrt(variance)

print("mean: " + str(mean))
print("median: " + str(median))
print("max: " + str(max))
print("min: " + str(min))
print("variance: " + str(variance))
print("standard deviation: " + str(std_dev))
print("positive number count: " + str(count_pos))
print("negative number count: " + str(count_neg))
