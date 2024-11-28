# Read a number from console. The number will be the length of the Fibonacci sequence to
# generate. Fibonacci is a sequence of numbers where the next number in the sequence is the sum
# of the previous two numbers in the sequence

import sys

if len(sys.argv) != 2:
    sys.exit("usage: " + sys.argv[0] + " <length of sequence>")

fibonacci = []
for i in range(int(sys.argv[1])):
    if i <= 1:
        fibonacci.append(1)
    else:
        a = fibonacci[len(fibonacci) - 1]
        b = fibonacci[len(fibonacci) - 2]
        fibonacci.append(a + b)

print(fibonacci)
