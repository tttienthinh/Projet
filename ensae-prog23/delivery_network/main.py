from graph import Graph, graph_from_file
import graphviz
import osmnx as ox

G = ox.graph_from_place("Palaiseau, France", network_type="drive")
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)


palaiseau = Graph.from_gpd_to_graph(gdf_edges, gdf_nodes)
#print(palaiseau.nodes, '\n', palaiseau.graph)
print(palaiseau.get_path_with_power(src=198859754, dest=218231906, power=300))



"""
test = graph_from_file("input/network.00.in")
a = test.kruskal()
print(a.calc_height_tree(root=3, dict={3:None}))
a.oriented_tree()
print(a.tree)
print("this is power_2puis", a.power_2puiss)
print(a.kruskal_2puiss_min_power(1, 3))
"""
"""
data_path = "input/"
file_name = "network.00.in"

g = graph_from_file(data_path + file_name)
g.connected_components()
# Le premier nombre est la puissance le deuxième est la distance
g.to_graphviz(file_name, view=False, src=1, dest=4)
a = g.kruskal()
print(a.graph)
a.to_graphviz(f"{file_name}-kruskal", view=False, src=1, dest=4)


test = graph_from_file("input/network.1.in")
print(test.get_path_with_power(6, 11, 15), 15)
print(test.get_path_with_power(6, 11, 18), 18)
a = test.kruskal()
a.oriented_tree()
print(a.kruskal_min_power(6, 11))
"""