# encoding: utf-8

from gurobipy import *
import parameters

model = Model("Trabajo pais")

# Variables
X = model.addVars(parameters.volunteers, parameters.locations, vtype=GRB.BINARY, name="assigned_to_community")
Y = model.addVars(parameters.volunteers, parameters.tasks, vtype=GRB.BINARY, name="assigned_to_task")
W = model.addVars(parameters.volunteers, parameters.tasks, parameters.locations, vtype=GRB.BINARY, name="assigned_to_community_on_task")
O = model.addVars(parameters.locations, vtype=GRB.BINARY, name="assign_community")
#? A
#? F
#? H
J = model.addVars(parameters.locations, vtype=GRB.BINARY, name="assigned_to_group")

# Actualización del modelo
model.update()

# Restricciones
# Cumplir con el presupuesto
#! Esta restricción cambió
model.addConstrs((quicksum(parameters.locations_dict[location]["Costo traslado"] * O[location] for location in parameters.locations) - 
    (1/3)*quicksum(parameters.locations_dict[location]["Costo traslado"] * J[location] for location in parameters.locations if location not in parameters.locations_plane) <= parameters.budget),
    name="r2")

# Tamaño de los grupos
model.addConstrs((quicksum(X[volunteer][location] for volunteer in parameters.volunteers) <= parameters.locations_dict[location]["Capacidad máxima"] * O[location] for location in parameters.locations), 
    name="r3")
model.addConstrs((quicksum(X[volunteer][location] for volunteer in parameters.volunteers) >= parameters.locations_dict[location]["Voluntarios mínimos"] * O[location] for location in parameters.locations), 
    name="r4")

# Voluntarios pueden pertenecer a una sola misión
model.addConstrs((quicksum(X[volunteer][location] for volunteer in parameters.volunteers) == 1 for location in parameters.locations),
    name="r5")

# Voluntarios son asignados a una tarea
model.addConstrs((quicksum(Y[volunteer][task] for task in range(1, 6)) == 1 for volunteer in parameters.volunteers),
    name="r6")

# Distancia a servicios más cercanos
model.addConstrs((parameters.locations_dict[location]["Distancia a posta más cercana (km)"] * O[location] <= parameters.locations_dict[location]["Distancia máxima aceptable a posta"] for location in parameters.locations),
    name="r7-1")
model.addConstrs((parameters.locations_dict[location]["Distancia a alimentos"] * O[location] <= parameters.locations_dict[location]["Distancia máxima a alimentos"] for location in parameters.locations),
    name="r7-2")



# función objetivo
#! Se está ocupando pandas, puede que sea necesario cambiarlo
obj = quicksum(
    parameters.volunteers_info.iloc[volunteer]["hability_{}".format(task)] * Y[volunteer][task]
    for volunteer in parameters.volunteers
    for task in range(1, 6)
)
model.setObjective(obj, GRB.MAXIMIZE)

if __name__ == "__main__":
    model.optimize()
    model.printAttr("X")
