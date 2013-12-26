import unittest
import copy
from automata.graph_operatations import * 


class GraphOperationsTest(unittest.TestCase):

    graph = {'A': {'B', 'C'},
             'B': {'C', 'D'},
             'C': {'D'},
             'D': {'C'},
             'E': {'F'},
             'F': {'C'}}

    def test_add_vertex(self):
        g = add_vertex(copy.deepcopy(GraphOperationsTest.graph), 'X')
        expected = {'A': {'B', 'C'},
                    'B': {'C', 'D'},
                    'C': {'D'},
                    'D': {'C'},
                    'E': {'F'},
                    'F': {'C'},
                    'X': set()}
        self.assertDictEqual(g, expected)

    def test_add_existing_vertex(self):
        g = add_vertex(copy.deepcopy(GraphOperationsTest.graph), 'E')
        self.assertDictEqual(g, GraphOperationsTest.graph)

    def test_add_edge(self):
        g = add_edge(copy.deepcopy(GraphOperationsTest.graph), 'A', 'E', directed=False)
        expected = {'A': {'B', 'C', 'E'},
                    'B': {'C', 'D'},
                    'C': {'D'},
                    'D': {'C'},
                    'E': {'F', 'A'},
                    'F': {'C'}}
        self.assertDictEqual(expected, g)

    def test_add_existing_edge(self):
        g = add_edge(copy.deepcopy(GraphOperationsTest.graph), 'A', 'B')
        self.assertDictEqual(g, GraphOperationsTest.graph)

    def test_find_closest(self):
        e = find_closest(GraphOperationsTest.graph, 'A', lambda x: x >= 'D')
        self.assertEqual(e, 'D')
        e = find_closest(GraphOperationsTest.graph, 'A', lambda x: x != 'C')
        self.assertEqual(e, 'A')
        e = find_closest(GraphOperationsTest.graph, 'A', lambda x: x >= 'Z')
        self.assertIsNone(e)
