# À compléter
# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network/")

import unittest 
from graph import Graph, graph_from_file

class Test_GraphLoading(unittest.TestCase):
    def test_network4(self):
        g = graph_from_file("input/network.04.in")
        #### refaire les test là c'est ceux d'un autre test pour l'instant
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 4)
        self.assertEqual(g.graph[1][0][2], 6)

if __name__ == '__main__':
    unittest.main()
