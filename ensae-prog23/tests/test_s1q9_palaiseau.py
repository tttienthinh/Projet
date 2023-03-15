import sys 
sys.path.append("delivery_network")

from graph import Graph
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

