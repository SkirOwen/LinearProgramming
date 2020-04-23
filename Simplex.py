from imports import *


x1 = pulp.LpVariable("x1", 0)
x2 = pulp.LpVariable("x2", 0)
x3 = pulp.LpVariable("x3", 0)
x4 = pulp.LpVariable("x4", 0)
# x5 = pulp.LpVariable("x5", 0)


prob = pulp.LpProblem("Morra", pulp.LpMaximize)

prob += -x1 - x2 - x3 - x4
prob += 8*x1 + 2*x2 + 6*x3 + 5*x4 >= 1
prob += 5*x1 + 12*x2 + 3*x3 + 5*x4 >= 1
prob += 4*x1 + 1*x2 + 8*x3 + 11*x4 >= 1
prob += 7*x1 + 8*x2 + 5*x3 + 12*x4 >= 1
# prob += 3*x1 + 2*x2 + 1*x3 + 1*x4 + 3*x5 <= 1
# prob += 1*x1 + 3*x2 + 2*x3 + 3*x4 + 1*x5 <= 1
# prob += 1*x1 + 3*x2 + 1*x3 + 2*x4 + 3*x5 <= 1
# prob += 3*x1 + 1*x2 + 3*x3 + 1*x4 + 2*x5 <= 1

status = prob.solve()

print("\n x1 = ", pulp.value(x1),
      "\n x2 = ", pulp.value(x2),
      "\n x3 = ", pulp.value(x3),
      "\n x4 = ", pulp.value(x4),
      # "\n x5 = ", pulp.value(x5),
      "\n")
print(pulp.LpStatus[status], "\n")

z = [pulp.value(x1),
         pulp.value(x2),
         pulp.value(x3),
         pulp.value(x4),
         ]

zt = sum(z)

print("z = ", zt, "\n v = ", 1/zt)
print(*[i/zt for i in z])

#
# OPTIMAL SOLUTION
# x*
# = (60/731, 18/731, 0, 1/17, 0, 0, 0, 349/731)
# z*
# = -121/731
