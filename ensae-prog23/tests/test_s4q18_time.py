# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import graph_from_file
from s4_q18 import kruskal_from_file, route_from_file, truck_from_file, tout_sous_ensemble
import unittest   # The test framework
import time
import matplotlib.pyplot as plt



data_path = "input/"
truck_name = f"trucks.0.in"

for i in range(1, 4):
    timing = [0]
    file_name = f"network.{i}.in"
    route_name = f"routes.{i}.in"
    a = kruskal_from_file(data_path + file_name)
    routes = route_from_file(data_path + route_name)
    trucks = truck_from_file(data_path + truck_name)
    for j in range(1, 15):
        start = time.time()
        tout_sous_ensemble(a, routes[:j], trucks, budget=25e9)
        timing.append(time.time()-start)
    plt.plot(timing, label=file_name)

plt.legend()
plt.grid()
plt.xlabel("Nombre de routes")
plt.ylabel("Temps d'éxecution en sec")
plt.title("Temps d'éxecution pour l'algorithme naif")
plt.savefig("tests/test_s4q18_time_naif.png")

