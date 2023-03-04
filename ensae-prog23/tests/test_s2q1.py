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
i = 2
for i in range(1, 3):
    print(i)
    file_name = f"network.{i}.in"
    route_name = f"routes.{i}.in"
    g = graph_from_file(data_path + file_name)
    r = route_from_file(data_path + route_name)
    nb_execution = 10
    start = time.time()
    args = r[0]
    a = g.kruskal()
    a.oriented_tree()
    for args in r[:nb_execution]:
        print(g.get_path_with_power(*args))
    times.append(len(r)*(time.time()-start)/nb_execution)


for i, t in enumerate(times):
    print(f"Pour éxecuter routes.{i+1}.in cela prendrait : {round(t, 2)} s  soit {round(t/3600)}h")
""" Estimation des temps :
Pour éxecuter routes.1.in cela prendrait : 0.01 s
Pour éxecuter routes.2.in cela prendrait : 10161.81 s       soit 3h
Pour éxecuter routes.3.in cela prendrait : 51548.29 s       soit 14h
Pour éxecuter routes.4.in cela prendrait : 53132.62 s       soit 15h
Pour éxecuter routes.5.in cela prendrait : 23351.7 s        soit 6h
Pour éxecuter routes.6.in cela prendrait : 109105.69 s      soit 30h
Pour éxecuter routes.7.in cela prendrait : 95373.01 s       soit 26h
Pour éxecuter routes.8.in cela prendrait : 103037.05 s      soit 28h
Pour éxecuter routes.9.in cela prendrait : 9356648.81 s     soit 2600h  soit 108 jours
"""
