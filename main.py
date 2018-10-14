from gurobipy import *
import parameters

model = Model("Trabajo pais")

# Variables
x = model.addVars(parameters.voluntaries, parameters.communities, vtype=GRB.BINARY, name="assigned_to_community")
y = model.addVars(parameters.voluntaries, parameters.tasks, vtype=GRB.BINARY, name="assigned_to_task")
w = model.addVars(parameters.voluntaries, parameters.tasks, parameters.communities, vtype=GRB.BINARY, name="assigned_to_community_on_task")
o = model.addVars(parameters.communities, vtype=GRB.BINARY, name="assign_community")

# Actualización del modelo
model.update()

# Restricciones

# función objetivo
# obj = 
# model.setObjective(obj, GRB.MAXIMIZE)

if __name__ == "__main__":
    model.optimize()
    model.printAttr("X")
