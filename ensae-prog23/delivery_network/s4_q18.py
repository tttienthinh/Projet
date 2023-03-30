import sys 
import time
import random
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
            if truck is None:
                return None, None
            profit += route[2]
            budget_restant -= truck[1]
            if budget < 0:
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
        if profit is not None and profit > best_profit:
            best_profit = profit
            best_liste_truck = liste_trucks
            best_route = sous_ensemble
    return best_profit, best_liste_truck, best_route
        
def glouton(a, routes, trucks, budget): # O(nb_routes * log(nb_routes))
    routes_infos = []
    for src, dest, utilite in routes:
        truck = best_truck_for_route(a, src, dest, trucks)
        if truck is not None:
            power, price = truck
            routes_infos.append((src, dest, utilite, power, price, utilite/price))
    
    routes_infos.sort(key=lambda x: x[-1])

    best_profit = 0
    best_liste_truck = []
    best_route = []
    breaked = False
    for src, dest, utilite, power, price, ratio in routes_infos:
        if budget-price < 0:
            breaked = True
            break
        budget -= price
        best_profit += utilite
        best_liste_truck.append(power)
        best_route.append((src, dest, utilite))
    if breaked:
        print(f"Avec glouton nous trouvons une utilité de {best_profit} à {ratio*budget} près. Car il reste {budget} €")
    else:
        print(f"Avec glouton nous trouvons une utilité de {best_profit} ce qui est le meilleur car plus assez de route même si il reste {budget} €")
    return best_profit, best_liste_truck, best_route
    

        
        


def random_optimisation(a, routes, trucks, budget, execution_time):
    # this algorithm is not assured to work in case of little amount of routes
    allocated = []
    unallocated = []
    current_utilitie = 0
    for src, dest, utilite in routes:
        truck = best_truck_for_route(a, src, dest, trucks)
        if truck is not None:
            power, price = truck
            unallocated.append((src, dest, utilite, power, price))
    current_price = 0
    while current_price <= budget: # We allocate the truck to sature the budget
        new_price = current_price + unallocated[0][-1]
        if new_price <= budget:
            current_price = new_price
            current_utilitie += unallocated[0][2]
            allocated.append(unallocated[0])
            unallocated.pop(0)
        else:
            break
    start = time.time()
    while time.time() - start <= execution_time: # here start the random iteration to optimise
        temp_utilitie = current_utilitie
        temp_price = current_price
        nb_to_unallocate = int(random.uniform(0, 100))
        to_unallocate = []
        for i in range(nb_to_unallocate): # we set a list of index to unalocate randomly
            index = int(random.uniform(0, len(allocated)-1))
            if index not in to_unallocate:
                to_unallocate.append(index)
        to_unallocate.sort(reverse=True)
        for index in to_unallocate: # we calculte how utiliti and cost we loose with this unalocation
            temp_price -= allocated[index][-1]
            temp_utilitie -= allocated[index][2]
        to_realocate = []
        while temp_price <= budget: # we sature randomly the budget by realocating truck randomly
            index = int(random.uniform(0, len(unallocated)-1))
            if index not in to_realocate:
                to_realocate.append(index)
                if temp_price + unallocated[index][-1] < budget:
                    temp_price += unallocated[index][-1]
                    temp_utilitie += unallocated[index][2]
                else:
                    to_realocate.pop(-1)
                    to_realocate.sort(reverse=True)
                    break
        if temp_utilitie >= current_utilitie: # if this realocation is benefic, we do it
            current_utilitie = temp_utilitie
            current_price = temp_price
            for index in to_unallocate:
                unallocated.append(allocated[index])
                allocated.pop(index)
            for index in to_realocate:
                allocated.append(unallocated[index])
                unallocated.pop(index)
    return current_utilitie, current_price, allocated #when the asked execution time is over, we return the result


if __name__ == "__main__":
    data_path = "input/"
    file_name = f"network.10.in"
    route_name = f"routes.10.in"
    truck_name = f"trucks.2.in"
    a = kruskal_from_file(data_path + file_name)
    routes = route_from_file(data_path + route_name)
    trucks = truck_from_file(data_path + truck_name)
    import time


    #start = time.time()
    #print(tout_sous_ensemble(a, routes[:10], trucks, budget=25e9))
    #print(time.time()-start)
    
    #start = time.time()
    #print(glouton(a, routes, routes[:10], trucks, budget=25e9))
    #print(time.time()-start)

    start = time.time()
    print(random_optimisation(a, routes, trucks, budget=25e9, execution_time=10)[0])
    print("ceci est le temps d'execution",time.time() - start)
