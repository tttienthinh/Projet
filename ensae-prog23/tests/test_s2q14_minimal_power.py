# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import graph_from_file
import unittest   # The test framework

class Test_MinimalPower(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        a = g.kruskal()
        a.oriented_tree()
        self.assertEqual(a.kruskal_min_power(1, 4)[1], 11)
        self.assertEqual(a.kruskal_min_power(2, 4)[1], 10)

    def test_network1(self):
        g = graph_from_file("input/network.04.in")
        a = g.kruskal()
        a.oriented_tree()
        self.assertEqual(a.kruskal_min_power(1, 4)[1], 4)

    def test_network2(self):
        g = graph_from_file("input/network.02.in")
        a = g.kruskal()
        a.oriented_tree()
        self.assertEqual(a.kruskal_min_power(1, 4)[1], 4)

    def test_network3(self):
        g = graph_from_file("input/network.03.in")
        a = g.kruskal()
        a.oriented_tree()
        self.assertEqual(a.kruskal_min_power(1, 4)[1], 10)


if __name__ == '__main__':
    unittest.main()
