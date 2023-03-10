# This will work if ran from the root folder.
import sys
sys.path.append("delivery_network/")

import unittest
from graph import Graph, graph_from_file

class Test_recursive_parc_connex(unittest.TestCase):
    def test_network0(self):
        graph = graph_from_file("input/network.00.in")
        height = graph.recursive_parc_connex(root=1)
        self.assertEqual(height, {1: 0, 2: 1, 6: 1, 8: 1, 3: 2, 5: 2, 9: 2, 4: 3, 7: 3, 10: 4 })


if __name__ == '__main__':
    unittest.main()
