from imports import *

X = pd.read_csv('dataset/ACSDP5Y2016.DP05_data_with_overlays_2020-03-25T063508.csv',
                usecols=['NAME', 'DP05_0001E', 'DP05_0082E'])

N = 538     # Number of member in the electoral college

