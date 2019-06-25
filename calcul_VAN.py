import csv
from sympy.solvers import solve
from sympy import Symbol, N

with open('VAN_input.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = -1
    x = Symbol('x')
    expr = 0
    annees= []
    for row in csv_reader:
        if i > -1:
            print(row)
            expr1 = (int(row[2]) - int(row[1])) * (1 + x)**(10-i)
            expr = expr + expr1
            print(expr)
        i += 1

result = solve(expr)
print([N(solution) for solution in result])
