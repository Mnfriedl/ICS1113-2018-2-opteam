# encoding: utf-8

from gurobipy import *
import parameters

model = Model("Trabajo pais")

# Variables
X = model.addVars(parameters.volunteers, parameters.locations, vtype=GRB.BINARY, name="assigned_to_community")
Y = model.addVars(parameters.volunteers, range(1, 6), vtype=GRB.BINARY, name="assigned_to_task")
W = model.addVars(parameters.volunteers, range(1, 6), parameters.locations, vtype=GRB.BINARY, name="assigned_to_community_on_task")
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
# model.addConstrs((quicksum(parameters.locations_dict[location]["Costo traslado"] * O[location] for location in parameters.locations) - 
#     (1/3)*quicksum(parameters.locations_dict[location]["Costo traslado"] * J[location] for location in parameters.locations if location not in parameters.locations_plane) <= parameters.budget),
#     name="r2")

# Tamaño de los grupos
model.addConstrs((quicksum(X[(volunteer, location)] for volunteer in parameters.volunteers) <= parameters.locations_dict[location]["Capacidad máxima"] * O[location] for location in parameters.locations), 
    name="r3")
model.addConstrs((quicksum(X[(volunteer, location)] for volunteer in parameters.volunteers) >= parameters.locations_dict[location]["Voluntarios mínimos"] * O[location] for location in parameters.locations), 
    name="r4")

# Voluntarios pueden pertenecer a una sola misión
model.addConstrs((quicksum(X[(volunteer, location)] for volunteer in parameters.volunteers) == 1 for location in parameters.locations),
    name="r5")

# Voluntarios son asignados a una tarea
model.addConstrs((quicksum(Y[(volunteer, task)] for task in range(1, 6)) == 1 for volunteer in parameters.volunteers),
    name="r6")

# Distancia a servicios más cercanos
model.addConstrs((parameters.locations_dict[location]["Distancia a posta más cercana (km)"] * O[location] <= parameters.locations_dict[location]["Distancia máxima aceptable a posta"] for location in parameters.locations),
    name="r7-1")
model.addConstrs((parameters.locations_dict[location]["Distancia a alimentos"] * O[location] <= parameters.locations_dict[location]["Distancia máxima a alimentos"] for location in parameters.locations),
    name="r7-2")

# Facilidad de acceso
model.addConstrs((parameters.locations_dict[location]["Distancia al lugar de construcción"] * O[location] <= parameters.max_distance_to_construction for location in parameters.locations),
    name="r8")

# Cantidad de hombres / mujeres por comunidad
model.addConstrs((quicksum(X[volunteer, location] * parameters.volunteers_info.iloc[volunteer]["gender"] for volunteer in parameters.volunteers) <= (parameters.mu / 100) * quicksum(X[volunteer, location] for volunteer in parameters.volunteers) for location in parameters.locations),
    name="r9")
model.addConstrs((quicksum(X[volunteer, location] * (1 - parameters.volunteers_info.iloc[volunteer]["gender"]) for volunteer in parameters.volunteers) <= (parameters.delta / 100) * quicksum(X[volunteer, location] for volunteer in parameters.volunteers) for location in parameters.locations),
    name="r10")

# Cantidad de personas de la misma carrera por comunidad
model.addConstrs((quicksum(X[volunteer, location] * (1 if parameters.volunteers_info.iloc[volunteer][career] == career else 0) for volunteer in parameters.volunteers) <= parameters.gamma for location in parameters.locations for career in parameters.careers),
    name="r11")

# Cantidad de personas por tarea por comunidad
model.addConstrs((quicksum(W[volunteer, task, location] for volunteer in parameters.volunteers) <= parameters.tasks_info.iloc[parameters.locations.index(location)]["min_vols_task_{}".format(task)] for location in parameters.locations for task in range(1, 6)),
    name="r12")

# función objetivo
obj = quicksum(
    parameters.volunteers_info.iloc[volunteer]["hability_{}".format(task)] * Y[(volunteer, task)]
    for volunteer in parameters.volunteers
    for task in range(1, 6)
)
model.setObjective(obj, GRB.MAXIMIZE)

if __name__ == "__main__":
    model.optimize()
    model.printAttr("X")
