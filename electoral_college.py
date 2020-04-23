from imports import *

path = os.path.join("./dataset", "ACSDP5Y2016.DP05_data_with_overlays_2020-03-25T063508.csv")

df = pd.read_csv(path, usecols=['NAME', 'DP05_0001E', 'DP05_0082E'])

# First row to header
df.columns = df.iloc[0]
df = df.reindex(df.index.drop(0)).reset_index(drop=True)

# Add a column of current electors for each sates
current_vote_rep = pd.Series([9, 3, 11, 6, 55, 9, 7, 3, 3, 29, 16, 4, 4, 20, 11, 6, 6,
                              8, 8, 4, 10, 11, 16, 10, 6, 10, 3, 5, 6, 4, 14, 5, 29, 15,
                              3, 18, 7, 7, 20, 4, 9, 3, 11, 38, 6, 3, 13, 12, 5, 10, 3]
                             )

df["Current Electors"] = current_vote_rep
# df[-1] Puerto Rico

n = 538  # Number of member in the electoral college
a_b = {}

# Creating the problem
u = pulp.LpVariable("u", 0)
v = pulp.LpVariable("v", 0)
a = pulp.LpVariable.dicts('a', (i for i in range(51)), lowBound=3, upBound=538-(50*3), cat=pulp.LpInteger)


prob = pulp.LpProblem("Electoral_College", pulp.LpMinimize)

prob += u - v

for i in range(len(df)-1):
    # prob += v <= a_b[i]
    prob += a[i] * 1000000/(float(df.iloc[i, 1])) >= v
    prob += a[i] * 1000000/(float(df.iloc[i, 1])) <= u

prob += pulp.lpSum(a[j] for j in range(len(a))) == n

prob.solve()

print(pulp.LpStatus[prob.solve()], "\n")

print("u = ", pulp.value(u), "\n v = ", pulp.value(v))
print("u-v = ", pulp.value(u) - pulp.value(v))
print("N = ", pulp.lpSum(pulp.value(a[j]) for j in range(len(a))))


for i in range(len(a)):
    print("a = ", (pulp.value(a[i])))


for i in range(51):
    if pulp.value(a[i]) == int(df.iloc[i, 3]):
        print("{0:20} {1}".format(df.iloc[i, 0], ("yep", df.iloc[i, 3], " -> ", pulp.value(a[i]))))
    else:
        print("\33[31m", "{0:20} {1}".format(df.iloc[i, 0], (df.iloc[i, 3], " -> ", pulp.value(a[i]))), "\33[0m")

old = [df.iloc[i, 3] / int(df.iloc[i, 1]) for i in range(51)]
print("min = ", min(old), "\n max = ", max(old))
print("max - min = ", max(old) - min(old))

print("-----------------------------------------------------")
new = [pulp.value(a[i]) / int(df.iloc[i, 1]) for i in range(51)]
print("min = ", min(new), "\n max = ", max(new))
print("max - min = ", max(new) - min(new))

print("-----------------------------------------------------")
print("max i = ", old.index(max(old)), "min i = ", old.index(min(old)))
print("max i = ", new.index(max(new)), "min i = ", new.index(min(new)))
