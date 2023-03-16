# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import graph_from_file
from s4_q18 import kruskal_from_file, route_from_file, truck_from_file, tout_sous_ensemble
import unittest   # The test framework

class Test_MinimalPower(unittest.TestCase):
    def test_network1(self):
        data_path = "input/"
        file_name = f"network.1.in"
        route_name = f"routes.1.in"
        truck_name = f"trucks.0.in"
        a = kruskal_from_file(data_path + file_name)
        routes = route_from_file(data_path + route_name)
        trucks = truck_from_file(data_path + truck_name)
        self.assertEqual(tout_sous_ensemble(a, routes[:3], trucks, budget=25e9)[0], 26034)

    def test_network3(self):
        data_path = "input/"
        file_name = f"network.3.in"
        route_name = f"routes.3.in"
        truck_name = f"trucks.0.in"
        a = kruskal_from_file(data_path + file_name)
        routes = route_from_file(data_path + route_name)
        trucks = truck_from_file(data_path + truck_name)
        profit, liste_truck, liste_route = tout_sous_ensemble(a, routes[:3], trucks, budget=25e9)
        self.assertEqual(profit, 11421)
        self.assertEqual(len(liste_truck), 2)
        self.assertEqual(len(liste_route), 2)


if __name__ == '__main__':
    unittest.main()
