import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from gurobipy import *

no_of_vehicles = 4  
df = pd.read_csv("VRPTW25.txt", ' ')
Y = list(df["Y"]);X = list(df["X"]);Demand = list(df["Demand"]);
coordinates = np.column_stack((X, Y))
n = len(coordinates)
m = Model("MVRP")
x = {};y = {}
dist_matrix = np.empty([n, n]) 
for i in range(n):
    for j in range(n):
        x[i, j] = m.addVar(vtype=GRB.BINARY, name="x%d,%d" % (i, j)) # 决策变量，公式1
        dist_matrix[i, j] = np.sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2) # 距离矩阵
for j in range(n):
    y[j] = m.addVar(vtype=GRB.INTEGER, name="y%d" % (j)) # 决策变量
m.setObjective(quicksum(quicksum(x[(i, j)] * dist_matrix[(i, j)] for j in range(n)) for i in range(n)),GRB.MINIMIZE) # 目标函数, 公式2    
m.addConstr(quicksum(x[(0, j)] for j in range(n)) == no_of_vehicles) # 约束条件1，公式3
m.addConstr(quicksum(x[(i, 0)] for i in range(n)) == no_of_vehicles) # 约束条件2，公式4
for i in range(n - 1):
    m.addConstr(quicksum(x[(i + 1, j)] for j in range(n)) == 1) # 约束条件3，公式5
for j in range(n - 1):
    m.addConstr(quicksum(x[(i, j + 1)] for i in range(n)) == 1) # 约束条件4，公式6

for j in range(n - 1): # 约束条件5，公式8
    for i in range(n - 1):
        m.addConstr(y[j] >= y[i] + 65 * x[i+1, j+1]-50)

m.update();m.optimize()
print('\n minimum distance: %g' % m.objVal)
m.printAttr('x')
from_node = []
to_node = np.empty([n, n])

for v in m.getVars():
    from_node.append(v.x)
for i in range(n):
    for j in range(n):
        to_node[i, j] = from_node[n * i + j]
I = [];J = []
for i in range(n):
    for j in range(n):
        if to_node[i, j] > 0.5:
            I.append(i)
            J.append(j)
XX1 = [];XX2 = [];YY1 = [];YY2 = []
for i in I:
    XX1.append(X[i])
    YY1.append(Y[i])
for j in J:
    XX2.append(X[j])
    YY2.append(Y[j])
plt.scatter(X,Y,marker='o', color='blue')
plt.xlabel('x-coordinate')
plt.ylabel('y-coordinate')
plt.plot([XX1, XX2], [YY1, YY2])
plt.show()