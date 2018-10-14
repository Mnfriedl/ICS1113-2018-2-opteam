import pandas as pd

volunteers_info = pd.read_csv("./volunteers.csv")
locations_info = pd.read_csv("./localidades.csv")
locations_info = locations_info.set_index("Localidad")
distances = pd.read_csv("./distancias_localidades.csv")
tasks_info = pd.read_csv("./tasks_per_location.csv")
distances = distances.set_index("Localidad")

volunteers = volunteers_info["volunteer_id"].tolist()
careers = volunteers_info["career"].unique().tolist()
locations = locations_info.index.tolist()
locations_plane = ["Pindaco", "Folilco"]
locations_dict = locations_info.T.to_dict()
distances_dict = distances.T.to_dict()

budget = 1000000
mu = 5
delta = 5
gamma = 5
max_distance_to_construction = 10
max_distance_between_communities = 5000
k = 590000

if __name__ == "__main__":
    print(distances_dict)
