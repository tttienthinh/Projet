import sys 
sys.path.append("delivery_network/")

from graph import Graph, graph_from_file

def route_from_file(filename):
    with open(filename) as file:
        nb_route = int(file.readline())
        routes = []
        for _ in range(nb_route):
            node1, node2, utile = file.readline().split()
            routes.append((int(node1), int(node2), float(utile)))
        file.close()
        return routes

def truck_from_file(filename):
    with open(filename) as file:
        nb_truck = int(file.readline())
        trucks = []
        for _ in range(nb_truck):
            power, price = file.readline().split()
            trucks.append((int(power), int(price)))
        file.close()
        # We only want cheapest truck, for a given power
        trucks.sort(key = lambda x: (x[0], -x[1]))
        trucks_filtre = [trucks[-1]]
        for elt in trucks[-2::-1]:
            if elt[1] < trucks_filtre[-1][1]:
                trucks_filtre.append(elt)
        return trucks_filtre[::-1] # cheapest trucks sorted by power

def kruskal_from_file(filename):
    g = graph_from_file(filename)
    a = g.kruskal()
    a.oriented_tree()
    return a


"""
Ici commence nos tentatives
"""
def best_truck_for_power(power, trucks): # Recherche dichotomique du meilleure camion
    if trucks == []:
        return None
    n = len(trucks)
    if n == 1:
        if trucks[0][0] >= power:
            return trucks[0]
        else:
            return None
    k = (n-1)//2
    if trucks[k][0] >= power:
        return best_truck_for_power(power, trucks[:(k+1)])
    else:
        return best_truck_for_power(power, trucks[(k+1):])

def best_truck_for_route(a, src, dest, trucks):
    power = a.kruskal_2puiss_min_power(src, dest)
    return best_truck_for_power(power, trucks)




def tout_sous_ensemble(a, routes, trucks, budget): # complexity O(log2^nb_route)
    """
    On va parcourir tous les sous-ensemble non vide de route, 
    voir quel sous ensemble possible est le plus profitable
    """
    def utilite(sous_ensemble, budget_restant): # calcul du profit si le sous-ensemble est possible
        liste_trucks = []
        profit = 0
        for route in sous_ensemble:
            truck = best_truck_for_route(a, route[0], route[1], trucks)
            profit += route[2]
            budget_restant -= truck[1]
            if truck is None or budget < 0:
                return None, None
            liste_trucks.append(truck)
        return liste_trucks, profit

        

    best_profit = 0
    best_liste_truck = []
    best_route = []
    for i in range(1, 2**len(routes)): # Il y a 2^nb_routes - 1 sous_ensemble, représentation binaire
        sous_ensemble = []
        nombre_decimal = i
        j = 0
        while nombre_decimal != 0:
            if nombre_decimal % 2 == 1:
                sous_ensemble.append(routes[j])
            nombre_decimal = nombre_decimal // 2
            j += 1
        
        liste_trucks, profit = utilite(sous_ensemble, budget)
        if profit > best_profit:
            best_profit = profit
            best_liste_truck = liste_trucks
            best_route = sous_ensemble
    return best_profit, best_liste_truck, best_route
        





if __name__ == "__main__":
    data_path = "input/"
    file_name = f"network.1.in"
    route_name = f"routes.1.in"
    truck_name = f"trucks.0.in"
    a = kruskal_from_file(data_path + file_name)
    routes = route_from_file(data_path + route_name)
    trucks = truck_from_file(data_path + truck_name)
    print(tout_sous_ensemble(a, routes[:3], trucks, budget=25e9))
