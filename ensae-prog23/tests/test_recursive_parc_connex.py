# This will work if ran from the root folder.
import sys
sys.path.append("delivery_network/")

import unittest
from graph import Graph, graph_from_file

class Test_recursive_parc_connex(unittest.TestCase):
    def test_network0(self):
        graph = graph_from_file("input/network.00.in")
        height = graph.recursive_parc_connex(root=1)
        self.assertTrue((1, 0) in height)
        self.assertTrue((2, 1) in height)
        self.assertTrue((6, 1) in height)
        self.assertTrue((8, 1) in height)
        self.assertTrue((3, 2) in height)
        self.assertTrue((5, 2) in height)
        self.assertTrue((9, 2) in height)
        self.assertTrue((4, 3) in height)
        self.assertTrue((7, 3) in height)
        self.assertTrue((10, 4) in height)# add assertion here


if __name__ == '__main__':
    unittest.main()
