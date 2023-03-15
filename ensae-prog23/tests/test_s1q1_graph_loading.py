# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network/")

import unittest 
from graph import Graph, graph_from_file

class Test_GraphLoading(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 9)

    def test_network1(self):
        g = graph_from_file("input/network.01.in")
        self.assertEqual(g.nb_nodes, 7)
        self.assertEqual(g.nb_edges, 5)

    def test_network2(self):
        g = graph_from_file("input/network.02.in")
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 4)
    
    def test_network3(self):
        g = graph_from_file("input/network.03.in")
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 4)
        self.assertEqual(set(g.graph[1]), {(2, 10, 1), (4, 11, 1)})
        self.assertEqual(set(g.graph[2]), {(1, 10, 1), (3, 4, 1)})
        self.assertEqual(set(g.graph[3]), {(2, 4, 1), (4, 4, 1)})
        self.assertEqual(set(g.graph[4]), {(3, 4, 1), (1, 11, 1)})
    
    def test_network4(self):
        g = graph_from_file("input/network.04.in")
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 4)
        self.assertEqual(g.graph[1][0][2], 6)

if __name__ == '__main__':
    unittest.main()
