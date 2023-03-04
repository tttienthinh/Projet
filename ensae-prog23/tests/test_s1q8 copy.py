# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import graph_from_file
import unittest   # The test framework

class Test_MinimalPower(unittest.TestCase):
    def test_network1(self):
        g = graph_from_file("input/network.1.in")
        self.assertEqual(g.graph[1][0][0], 2)
        self.assertEqual(g.graph[1][0][1], 2)
        self.assertEqual(g.graph[1][0][2], 6312)
        self.assertEqual(g.graph[2][1][0], 3)
        self.assertEqual(g.graph[2][1][1], 5)
        self.assertEqual(g.graph[2][1][2], 6891)

    def test_network9(self):
        g = graph_from_file("input/network.9.in")
        self.assertEqual(g.graph[1][0][0], 2)
        self.assertEqual(g.graph[1][0][1], 10000)
        self.assertEqual(g.graph[1][0][2], 6630)
        self.assertEqual(g.graph[2][1][0], 3)
        self.assertEqual(g.graph[2][1][1], 100)
        self.assertEqual(g.graph[2][1][2], 3836)

if __name__ == '__main__':
    unittest.main()
