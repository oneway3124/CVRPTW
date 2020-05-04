import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from gurobipy import *

no_of_vehicles = 2
df = pd.read_csv("VRPTW11.txt", ' ')
X = list(df["X"])
Y = list(df["Y"])
coordinates = np.column_stack((X, Y))  # 从数据中取出X,Y,形成coordinates
# print(coordinates)
n = len(coordinates)
# print(n)
depot = coordinates[0, :]  # 起点的位置
# print(depot)
customers = coordinates[1:, :]  # 无线充电节点的位置
# print(customers)
# plt.scatter(X, Y)  # 可以将前面计算的节点以散点图的方式画图到plot上
# plt.show()
model = Model()  # gurobi构建模型
x = {}
dist_matrix = np.empty([n, n])
print(model)

for i in range(len(X)):
    for j in range(len(Y)):
        x[i, j] = model.addVar(vtype=GRB.BINARY)
        dist_matrix[i, j] = np.sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)
        if i == j:
            # dist_matrix = float('inf')
            dist_matrix[i, j] = 0
model.update()  # 更新决策变量

# 约束条件1
model.addConstr(quicksum(x[(0, j)] for j in range(len(coordinates))) == no_of_vehicles)
model.update()

# 约束条件2
model.addConstr(quicksum(x[(i, 0)] for i in range(len(coordinates))) == no_of_vehicles)
model.update()

# 约束条件3  只能转移到其中1个节点
for i in range(2, len(coordinates)):
    model.addConstr(quicksum(x[(i, j)] for j in range(2, len(coordinates))) == 1)
model.update()

# 约束条件4  只能从其中一个节点转移过来的
for j in range(2, len(coordinates)):
    model.addConstr(quicksum(x[(i, j)] for i in range(2, len(coordinates))) == 1)
model.update()

# 目标函数
model.setObjective(quicksum(
    (quicksum(x[(i, j)] * dist_matrix[(i, j)] for j in range(len(coordinates)))) for i in range(len(coordinates))),
    GRB.MINIMIZE)
model.update()

model.optimize()

solution = model.getAttr('x', x)
print('%g' % model.objVal)