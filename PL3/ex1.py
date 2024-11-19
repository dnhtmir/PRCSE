import math
squared_number = int(input("give me a number: "))
root = math.sqrt(squared_number)
if root % 1 == 0:
    print("is perfect square")
else:
    print("isn't perfect square")
