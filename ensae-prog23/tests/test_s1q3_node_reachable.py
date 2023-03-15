# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file

import unittest   # The test framework

class Test_Reachability(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        self.assertEqual(g.get_path_with_power(1, 4, 11), [1, 2, 3, 4])
        self.assertEqual(g.get_path_with_power(1, 4, 10), None)

    def test_network1(self):
        g = graph_from_file("input/network.01.in")
        self.assertEqual(g.get_path_with_power(1, 3, 11), [1, 2, 3])
        self.assertEqual(g.get_path_with_power(1, 4, 10), None)

    def test_network2(self):
        g = graph_from_file("input/network.02.in")
        self.assertIn(g.get_path_with_power(1, 2, 11), [[1, 2], [1, 4, 3, 2]])
        self.assertEqual(g.get_path_with_power(1, 2, 5), [1, 4, 3, 2])

    def test_network3(self):
        g = graph_from_file("input/network.03.in")
        self.assertEqual(g.get_path_with_power(1, 4, 10), [1, 2, 3, 4])
        self.assertEqual(g.get_path_with_power(1, 4, 9), None)

    def test_network4(self):
        g = graph_from_file("input/network.04.in")
        self.assertEqual(g.get_path_with_power(1, 4, 10), [1, 2, 3, 4])
        self.assertEqual(g.get_path_with_power(1, 5, 5), None)

if __name__ == '__main__':
    unittest.main()
