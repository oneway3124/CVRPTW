import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from gurobipy import *

Q = 62  # 汽车容量
no_of_vehicles = 2  # 路径条数
df = pd.read_csv("VRPTW11.txt", ' ')
X = list(df["X"])
Y = list(df["Y"])

coordinates = np.column_stack((X, Y))
n = len(coordinates)
depot = coordinates[0, :]
customers = coordinates[1:, :]

m = Model("MVRP")
x = {}
y = {}
z = {}
dist_matrix = np.empty([n, n])
# add variable 1
for i in range(len(X)):
    for j in range(len(Y)):
        x[i, j] = m.addVar(vtype=GRB.BINARY, name="x%d,%d" % (i, j))
        dist_matrix[i, j] = np.sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)
        if i == j:
            dist_matrix[i, j] = float('inf')
        continue
m.update()
# add variable 1
for j in range(len(coordinates)):
    y[j] = m.addVar(vtype=GRB.INTEGER, name="y%d" % (j))
    z[j] = m.addVar(vtype=GRB.INTEGER, name="z%d" % (j))
m.update()

# constraint 1
for i in range(len(coordinates) - 1):
    m.addConstr(quicksum(x[(i + 1, j)] for j in range(len(coordinates))) == 1)
m.update()



print(dist_matrix)
