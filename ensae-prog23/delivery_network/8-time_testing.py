from graph import Graph, graph_from_file
import matplotlib.pyplot as plt 
import time

data_path = "input/"
functions_to_tests = [ # name of the function to test and arguments
    ("connected_components", {}), 
    ("get_path_with_power", {"src":1, "dest":20, "power":100}), 
    ("min_power", {"src":1, "dest":20}), 
]
time_dict = {name:[] for name, _ in functions_to_tests}
for i in range(1, 11):
    file_name = f"network.{i}.in"
    g = graph_from_file(data_path + file_name)
    for name, kwargs in functions_to_tests:
        start = time.time()
        print(i, name, kwargs)
        getattr(g, name)(**kwargs)
        time_dict[name].append(time.time()-start)

for name, _ in functions_to_tests:
    plt.plot(time_dict[name], label=name)
plt.grid()
plt.xlabel("network.X.in")
plt.ylabel("Execution time in seconds")
plt.legend()
plt.savefig("delivery_network/8-time_result.png")

# Every functions is executing on the network.X.in within 0.6 sec

