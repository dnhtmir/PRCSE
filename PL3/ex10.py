# Read the “. json” file resultant of exercise 1 and determine the following metrics. Store this
# information as human-readable text in well formatted “.txt” file.
# c. For each department:
# i. The number of employees.
# ii. Average salary.
# iii. Early expenses based on base salary (14 months)
# d. For the company:
# i. Number of departments.
# ii. Departments with lowest and highest early wages.
# iii. Total amount of wage expenses.

import os
import sys
import json

if len(sys.argv) != 1:
    sys.exit("usage: " + sys.argv[0])

input_file = os.path.join(os.path.dirname(sys.argv[0]), 'ex9_test_artifacts', 'output.json')
if not os.path.exists(input_file):
    sys.exit("file output.json not found")

with open(os.path.join(input_file), 'r') as file:
    data = json.load(file)

dept_stats = {}
for dept, info in data.items():
    dept_stats[dept] = {} 
    emp_count = 0
    salary_total = 0
    yearly_expense = 0
    monthly_expense = 0
    for dept_data in info:
        emp_count += 1
        salary_total += float(dept_data['Salary'])
    
    dept_stats[dept]['NumberEmployees'] = emp_count
    dept_stats[dept]['AverageSalary'] = round(salary_total / emp_count, 2)
    dept_stats[dept]['YearlyExpenses'] = round(salary_total * 14, 2)
    dept_stats[dept]['MonthlyExpenses'] = round(salary_total, 2)

comp_dept_count = len(dept_stats)
comp_min_expense = min(dept_stats, key=lambda x: dept_stats[x]['YearlyExpenses'])
comp_max_expense = max(dept_stats, key=lambda x: dept_stats[x]['YearlyExpenses'])
comp_total_expenses = sum(dept_stats[dept]['YearlyExpenses'] for dept in dept_stats)

output_file = os.path.join(os.path.dirname(input_file), 'output.txt')
with open(output_file, 'w') as file:
    file.write('Company Metrics\n')
    file.write('Number of Departments: {}\n'.format(comp_dept_count))
    file.write('Department with Lowest Yearly Wages: {}\n'.format(comp_min_expense))
    file.write('Department with Highest Yearly Wages: {}\n'.format(comp_max_expense))
    file.write('Total Amount of Wage Expenses: {} €\n'.format(comp_total_expenses))
    file.write('\n')

    for dept, info in dept_stats.items():
        file.write('Department: {}\n'.format(dept))
        file.write('Number of Employees: {}\n'.format(info['NumberEmployees']))
        file.write('Average Salary: {} €\n'.format(info['AverageSalary']))
        file.write('Yearly Expenses: {} €\n'.format(info['YearlyExpenses']))
        file.write('Monthly Expenses: {} €\n'.format(info['MonthlyExpenses']))
        file.write('\n')
