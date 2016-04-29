from unittest.case import TestCase

from factory_boy_fixtures.fixtures.loader import Graph


class GraphTestCase(TestCase):

    def setUp(self):
        """
        Setup a graph with the following dependencies

        a -> d, b
        b -> c, e
        c -> d, e
        d ->
        e ->
        """
        self.graph = Graph()
        self.graph.add_node('a')
        self.graph.add_node('b')
        self.graph.add_node('c')
        self.graph.add_node('d')
        self.graph.add_node('e')

        self.graph.add_dependency('a', 'd')
        self.graph.add_dependency('a', 'b')

        self.graph.add_dependency('b', 'c')
        self.graph.add_dependency('b', 'e')

        self.graph.add_dependency('c', 'd')
        self.graph.add_dependency('c', 'e')

    def test_resolve_node(self):
        """
        Case: a node get resolved
        Expected: The dependencies of that node get returned first
        """
        flat_list = self.graph.resolve_node('c')
        self.assertListEqual(flat_list, ['d', 'e', 'c'])

    def test_resolve_node_without_start(self):
        """
        Case: Call resolve_node without parameters
        Expected: All dependencies should be returned in correct order.
        """
        flat_list = self.graph.resolve_node()
        self.assertListEqual(flat_list, ['d', 'e', 'c', 'b', 'a'])

    def test_iterator(self):
        """
        Case: Iterate through the graph
        Expected: the dependent nodes get returned first
        """
        flat_list = [item for item in self.graph]
        self.assertListEqual(flat_list, ['d', 'e', 'c', 'b', 'a'])

    def test_circular_dependency(self):
        """
        Case: a circular dependency is configured
        Expected: An error get raised
        """
        self.graph.add_dependency('c', 'a')
        with self.assertRaises(Exception) as e:
            self.graph.resolve_node()
        self.assertEqual(e.exception.args[0] % e.exception.args[1:],
                         'Circular dependency c > a')
