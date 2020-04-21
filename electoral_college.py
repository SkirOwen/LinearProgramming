from imports import *

df = pd.read_csv('dataset/ACSDP5Y2016.DP05_data_with_overlays_2020-03-25T063508.csv',
                usecols=['NAME', 'DP05_0001E', 'DP05_0082E'])

# First row to header
df.columns = df.iloc[0]
df = df[1:]

N = 538     # Number of member in the electoral college

