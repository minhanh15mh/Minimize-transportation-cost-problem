from pulp import *
import pandas as pd  
import numpy as np  
n_warehouse = 4
n_factory = 3
#cost matrix
cost_matrix =  np.array([[250,420,380,280],[1280,990,1440,1520],[1550,1420,1660,1730]])
#production matrix
factory_quantity= np.array([45,120,95])
warehouse_demand = np.array([80,78,47,55])
model=LpProblem('transportation cost problem', LpMinimize)
#define decision variables
variable_name = [str(i)+str(j)for j in range(1,n_warehouse+1) for i in range(1,n_factory+1)]
variable_name.sort()
print('variable indices: ',variable_name)
#variable scope
dv_variable= LpVariable.matrix('X',variable_name,cat='Integer', lowBound=0)
allocation= np.array(dv_variable).reshape(3,4)
print('decision variable/ allocation matrix: ',allocation)

#objetive function
obj_func= lpSum(allocation*cost_matrix)
print('objective function: ',obj_func)
model+=obj_func
print(model)

#warehouse demand constraints
for j in range (n_warehouse):
    print(lpSum(allocation[i][j] for i in range(n_factory)) == warehouse_demand[j])
    model+=lpSum(allocation[i][j] for i in range(n_factory)) == warehouse_demand[j]

#production quantities constraints:
for i in range(n_factory):
    print(lpSum(allocation[i][j] for j in range (n_warehouse))<=factory_quantity[i])
    model+=lpSum(allocation[i][j] for j in range(n_warehouse))<=factory_quantity[i]

#model solve
model.solve(PULP_CBC_CMD())
status= LpStatus[model.status]
print(status)

#output 
print('total cost: ',model.objective.value())
for v in model.variables():
    try:
        print(v.name, '=',v.value())
    except:
        print('error couldnt find value')
