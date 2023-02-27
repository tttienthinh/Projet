from graph import Graph, graph_from_file, kruskal
import graphviz

data_path = "input/"
file_name = "network.02.in"

g = graph_from_file(data_path + file_name)
g.connected_components()
g.get_path_with_power(1, 2, 10)
# Le premier nombre est la puissance le deuxième est la distance
g.to_graphviz(file_name)
a = kruskal(g)
a.to_graphviz(f"{file_name}-kruskal")