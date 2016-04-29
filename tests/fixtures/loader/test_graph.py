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
        flat_list = [item for item in self.graph.resolve_node('a', [])]
        self.assertListEqual(flat_list, ['d', 'e', 'c', 'b', 'a'])

    def test_iterator(self):
        """
        Case: Iterate through the graph
        Expected: the dependent nodes get returned first
        """
        flat_list = [item for item in self.graph]
        self.assertListEqual(flat_list,
                             ['d', 'e', 'c', 'b', 'a'])


