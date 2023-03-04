# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file
import matplotlib.pyplot as plt 
import time

def route_from_file(filename):
    with open(filename) as file:
        nb_route = int(file.readline())
        routes = [list(map(int, file.readline().split())) for _ in range(nb_route)]
        file.close()
        return routes

data_path = "input/"
times = []
for i in range(1, 10):
    print(i)
    file_name = f"network.{i}.in"
    route_name = f"routes.{i}.in"
    g = graph_from_file(data_path + file_name)
    r = route_from_file(data_path + route_name)
    start = time.time()
    a = g.kruskal()
    a.oriented_tree()
    lines = []
    nb_execution = 10
    for args in r:
        path, power_min = a.kruskal_min_power(args[0], args[1])
        lines.append(str(power_min))
    with open("output/"+route_name, "w") as file:
        file.write("\n".join(lines))
        file.close()
    times.append(time.time()-start)


for i, t in enumerate(times):
    print(f"Pour éxecuter routes.{i+1}.in cela prendrait : {round(t, 2)} s  soit {round(t/60)}min")

"""
Pour éxecuter routes.1.in cela prendrait : 0.0 s    soit 0min
Pour éxecuter routes.2.in cela prendrait : 2.14 s   soit 0min
Pour éxecuter routes.3.in cela prendrait : 62.61 s  soit 1min
Pour éxecuter routes.4.in cela prendrait : 58.67 s  soit 1min
Pour éxecuter routes.5.in cela prendrait : 15.04 s  soit 0min
Pour éxecuter routes.6.in cela prendrait : 76.57 s  soit 1min
Pour éxecuter routes.7.in cela prendrait : 73.12 s  soit 1min
Pour éxecuter routes.8.in cela prendrait : 60.61 s  soit 1min
Pour éxecuter routes.9.in cela prendrait : 68.0 s   soit 1min

Comparé aux estimations précédentes test_s2q1.py
On est vraiment plus efficace, en calculant l'arbre couvrant minimal et en l'orientant
"""