from gurobipy import *
from parameters.py import *

model = Model("Trabajo pais")

# Variables

# Actualización del modelo
model.update()

# Restricciones

# función objetivo
# obj = 
# model.setObjective(obj, GRB.MAXIMIZE)

if __name__ == "__main__":
    model.optimize()
    model.printAttr("X")
