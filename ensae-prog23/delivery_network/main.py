from graph import Graph, graph_from_file
import graphviz
import osmnx as ox

def get_lat_long_from_address(address):
    try:
        from geopy.geocoders import Nominatim # pip install geopy
        geolocator = Nominatim(user_agent="Palaiseau")
        location = geolocator.geocode(address)
        return location.latitude, location.longitude
    except:
        print("Vous ne possédez pas geopy : pip install geopy")
        if address == "45 Rue de la Sablière, Palaiseau":
            return 48.7257757, 2.2270015
        elif address == "ENSAE Paris, Avenue Le Chatelier, Palaiseau":
            return 48.7107625, 2.207946715842018
        else:
            print("Votre adresse n'est pas connue par nos service secret. Installer geopy !")

G = ox.graph_from_place("Palaiseau, France", network_type="drive")
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)


# Quel est le chemin optimal pour aller en cours ?
lat, long = get_lat_long_from_address("45 Rue de la Sablière, Palaiseau") # L'adresse d'Aimé
src = ox.distance.nearest_nodes(G, X=long, Y=lat)
lat, long = get_lat_long_from_address("ENSAE Paris, Avenue Le Chatelier, Palaiseau") # L'adresse de l'ENSAE
dest = ox.distance.nearest_nodes(G, X=long, Y=lat)
route = ox.shortest_path(G, src, dest)
fig, ax = ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k')
fig.savefig("tests/test_s1_q9_palaiseau.png")

# Quel est le chemin optimal avec notre graphe ?
palaiseau = Graph.from_gpd_to_graph(gdf_edges, gdf_nodes)
path = palaiseau.get_path_with_power(src=src, dest=dest, power=300)

# Les différences sont dûes à la prise en compte des sens interdits
print(route)
print(path)


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