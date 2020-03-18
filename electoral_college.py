from pulp import *

x = LpVariable("x", 0)
y = LpVariable("y", 0)

prob = LpProblem("myProblem", LpMinimize)
prob += -8*x-5*y
prob += x + y <= 6
prob += 9*x+5*y <= 45

status = prob.solve()

print(value(x))
