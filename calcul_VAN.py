import csv
from sympy.solvers import solve
from sympy import Symbol, N, real_roots, plot
from sympy.solvers.inequalities import solve_poly_inequality

with open('VAN_input.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = -1
    x = Symbol('x', real="True")
    expr = 0
    annees= []
    for row in csv_reader:
        if i > -1:
            print(row)
            expr1 = (int(row[2]) - int(row[1])) * (1 + x)**(11-i)
            expr = expr + expr1
            print(expr)
        i += 1

result = solve(expr, x)

print([solution.n(2) for solution in result])

expr2 = expr / (1+x)**11
plot(expr2, (x, 0, 1), ylabel='Discount rate')