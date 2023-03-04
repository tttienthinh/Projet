from graph import Graph, graph_from_file
import graphviz

data_path = "input/"
file_name = "network.04.in"

g = graph_from_file(data_path + file_name)
g.connected_components()
# Le premier nombre est la puissance le deuxième est la distance
g.to_graphviz(file_name, view=False)
a = g.kruskal()
print(a.graph)
a.to_graphviz(f"{file_name}-kruskal", view=False)