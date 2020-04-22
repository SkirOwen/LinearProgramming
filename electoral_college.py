from imports import *

N = 538  # Number of member in the electoral college
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

# Creating the problem
u = pulp.LpVariable("u", 0)
v = pulp.LpVariable("v", 0)

prob = pulp.LpProblem("Electoral_College", pulp.LpMinimize)

prob += u - v

for i in range(len(df)-1):
    prob += v <= int(df.iloc[i, 3]) / int(df.iloc[i, 1])
    prob += u >= int(df.iloc[i, 3]) / int(df.iloc[i, 1])

status = prob.solve()
print(status)
print("u = ", pulp.value(u), "\n v = ", pulp.value(v))
print("u-v = ", pulp.value(u) - pulp.value(v))


for i in range(51):
    if pulp.value(v) <= int(df.iloc[i, 3])/int(df.iloc[i, 1]) <= pulp.value(u):
        print("{} \t yep".format(df.iloc[i, 0]))
    else:
        print("{} \t nope".format(df.iloc[i, 0]), "\t (", pulp.value(v), ";", pulp.value(u), ") ->", int(df.iloc[i, 3])/int(df.iloc[i, 1]))


