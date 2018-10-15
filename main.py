# encoding: utf-8

from gurobipy import *
import parameters
import json

model = Model("Trabajo pais")

# Variables
X = model.addVars(parameters.volunteers, parameters.locations, vtype=GRB.BINARY, name="assigned_to_community")
Y = model.addVars(parameters.volunteers, range(1, 6), vtype=GRB.BINARY, name="assigned_to_task")
W = model.addVars(parameters.volunteers, range(1, 6), parameters.locations, vtype=GRB.BINARY, name="assigned_to_community_on_task")
O = model.addVars(parameters.locations, vtype=GRB.BINARY, name="assign_volunteer_to_community")
A = model.addVars(parameters.locations, range(1, 10), vtype=GRB.BINARY, name="community_belongs_to_group")
F = model.addVars(parameters.locations, parameters.locations, range(1, 10), vtype=GRB.BINARY, name="both_communities_belong_to_group")
H = model.addVars(range(1, 10), vtype=GRB.BINARY, name="assign_community_to_group")
J = model.addVars(parameters.locations, vtype=GRB.INTEGER, name="assigned_to_group")

# Actualización del modelo
model.update()

# Restricciones
# Cumplir con el presupuesto
model.addConstr((quicksum(parameters.locations_dict[location]["Costo traslado"] * (O[location] - (1/3)*J[location]) for location in [x for x in parameters.locations if x not in parameters.locations_plane]) + quicksum(parameters.locations_dict[c]["Costo traslado"] * X[v, c] for c in parameters.locations_plane for v in parameters.volunteers) <= parameters.budget),
    name="r2")

# Tamaño de los grupos
model.addConstrs((quicksum(X[(volunteer, location)] for volunteer in parameters.volunteers) <= parameters.locations_dict[location]["Capacidad máxima"] * O[location] for location in parameters.locations), 
    name="r3")
model.addConstrs((quicksum(X[(volunteer, location)] for volunteer in parameters.volunteers) >= parameters.locations_dict[location]["Voluntarios mínimos"] * O[location] for location in parameters.locations), 
    name="r4")

# Voluntarios pueden pertenecer a una sola misión
model.addConstrs((quicksum(X[(volunteer, location)] for location in parameters.locations) == 1 for volunteer in parameters.volunteers),
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
model.addConstrs((quicksum(X[volunteer, location] * (1 if parameters.volunteers_info.iloc[volunteer]["career"] == career else 0) for volunteer in parameters.volunteers) <= parameters.gamma for location in parameters.locations for career in parameters.careers),
    name="r11")

# Cantidad de personas por tarea por comunidad
model.addConstrs((quicksum(W[volunteer, task, location] for volunteer in parameters.volunteers) >= parameters.tasks_info.iloc[parameters.locations.index(location)]["min_vols_task_{}".format(task)] * O[location] for location in parameters.locations for task in range(1, 6)),
    name="r12")

# Utilizar solo los primeros grupos
model.addConstrs((H[g] >= H[g + 1] for g in range(1, 9)),
    name="r13")

# Distancia máxima entre comunidades del mismo grupo
model.addConstrs((parameters.distances_dict[c1][c2] <= parameters.max_distance_between_communities + (1 - F[c1, c2, g]) * parameters.k for c1 in [x for x in parameters.locations if x not in parameters.locations_plane] for c2 in [x for x in parameters.locations if x not in parameters.locations_plane] if c1 != c2 for g in range(1, 10)),
    name="r14")

# Los grupos tienen 0 o 3 personas cada uno
model.addConstrs((quicksum(A[location, g] for location in [x for x in parameters.locations if x not in parameters.locations_plane]) == 3*H[g] for g in range(1, 10)),
    name="r15")

# Comunidades a las que no se irá no pertenecen a un grupo
model.addConstrs((J[location] <= O[location] for location in [x for x in parameters.locations if x not in parameters.locations_plane]),
    name="r16")

# Cada comunidad solo puede pertenecer a un grupo
model.addConstrs((J[location] <= 1 for location in [x for x in parameters.locations if x not in parameters.locations_plane]),
    name="r17")

# Relación entre variables
model.addConstrs((W[v, t, c] >= X[v, c] + Y[v, t] - 1 for v in parameters.volunteers for c in parameters.locations for t in range(1, 6)),
    name="r18")
model.addConstrs((W[v, t, c] <= X[v, c] for v in parameters.volunteers for c in parameters.locations for t in range(1, 6)),
    name="r19")
model.addConstrs((W[v, t, c] <= Y[v, t] for v in parameters.volunteers for c in parameters.locations for t in range(1, 6)),
    name="r20")
model.addConstrs((F[c1, c2, g] >= A[c1, g] + A[c2, g] - 1 for c1 in [x for x in parameters.locations if x not in parameters.locations_plane] for c2 in [x for x in parameters.locations if x not in parameters.locations_plane] for g in range(1, 10)),
    name="r21")
model.addConstrs((F[c1, c2, g] <= A[c1, g] for c1 in [x for x in parameters.locations if x not in parameters.locations_plane] for c2 in [x for x in parameters.locations if x not in parameters.locations_plane] for g in range(1, 10)),
    name="r22")
model.addConstrs((F[c1, c2, g] <= A[c2, g] for c1 in [x for x in parameters.locations if x not in parameters.locations_plane] for c2 in [x for x in parameters.locations if x not in parameters.locations_plane] for g in range(1, 10)),
    name="r23")
model.addConstrs((J[c] == quicksum(A[c, g] for g in range(1, 10)) for c in [x for x in parameters.locations if x not in parameters.locations_plane]),
    name="r24")

# Naturaleza de las variables
model.addConstrs((J[location] >= 0 for location in parameters.locations),
    name="nature")

# función objetivo
obj = quicksum(
    parameters.volunteers_info.iloc[volunteer]["hability_{}".format(task)] * Y[(volunteer, task)]
    for volunteer in parameters.volunteers
    for task in range(1, 6)
)
model.setObjective(obj, GRB.MAXIMIZE)

if __name__ == "__main__":
    model.optimize()
    #model.computeIIS()
    #model.write("model.sol")
    

