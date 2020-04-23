import pulp
import pandas

"""
x1 = pulp.LpVariable("x1",0)
x2 = pulp.LpVariable("x2", 0)

problem = pulp.LpProblem("Question 2 - 1", pulp.LpMinimize)
problem += x1 + x2 <= 6
problem += 9*x1 + 5*x2 <= 45
problem += -8*x1 - 5*x2

status = problem.solve()

print(pulp.value(x1), pulp.value(x2))
"""

u = pulp.LpVariable("u", 0)
v = pulp.LpVariable("v", 0)
# numberOfRepresentatives = 538

electoralCollege = pandas.read_csv("Electoral_College.csv", sep=';')
print(electoralCollege.head())

numberOfVotes = []
population = []

# extract a list of number of vote per state (index)
for stateNumberOfVotes in electoralCollege["Number of votes"]:
    numberOfVotes.append(stateNumberOfVotes)

# extract a list of number of pop per state (index)
for statePopulation in electoralCollege["Population"]:
    population.append(statePopulation)

print(*zip(numberOfVotes, population))

problem = pulp.LpProblem("Electoral College", pulp.LpMinimize)

for i in range(51):
    problem += v <= numberOfVotes[i]/population[i]
    problem += -u <= -numberOfVotes[i]/population[i]

problem += u-v

status = problem.solve()
uSol = pulp.value(u)
vSol = pulp.value(v)

for i in range(51):
    if pulp.value(v) <= numberOfVotes[i]/population[i] <= pulp.value(u):
        print("{} \t yep".format(electoralCollege.iloc[i, 0]))
    else:
        print("{} \t nope".format(electoralCollege.iloc[i, 0]), "\t (", pulp.value(v), ";", pulp.value(u), ") ->", numberOfVotes[i]/population[i])
