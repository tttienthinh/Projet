from graph import Graph, graph_from_file
import matplotlib.pyplot as plt 
import time

def route_from_file(filename):
    with open(filename) as file:
        nb_route = int(file.readline())
        routes = [map(int, file.readline().split()) for _ in range(nb_route)]
        return routes


data_path = "input/"
times = []
for i in range(1, 10):
    print(i)
    file_name = f"network.{i}.in"
    route_name = f"routes.{i}.in"
    g = graph_from_file(data_path + file_name)
    r = route_from_file(data_path + route_name)
    nb_execution = 10
    start = time.time()
    for args in r[:nb_execution]:
        print(g.get_path_with_power(*args))
    times.append(len(r)*(time.time()-start)/nb_execution)

print(times)
