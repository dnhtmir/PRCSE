# Consider a “.csv” file with 4 columns, Department, Name, Role, Salary. Read the file and
# organize the data into a dictionary (each department should be stored as key and the
# corresponding value should be a list of dictionaries containing employee’s name, role, and
# salary). Save the contents of the dictionary as an indented “. json” file.
# a. Hint: open(), split(), json.dump()
# b. What is JSON Standard?

import json
import os
import sys

if len(sys.argv) != 2:
    sys.exit("usage: " + sys.argv[0] + " <file.csv>")

input_file = sys.argv[1]

data = {}
with open(input_file, 'r') as file:
    lines = file.readlines()
    for line in lines[1:]:  # Skip the header
        department, name, role, salary = line.strip().split(',')
        if department not in data:
            data[department] = []
        data[department].append({
            'Name': name,
            'Role': role,
            'Salary': salary
        })

output_file = os.path.join(os.path.dirname(input_file), 'output.json')
with open(output_file, 'w') as json_file:
    json.dump(data, json_file, indent=4)
