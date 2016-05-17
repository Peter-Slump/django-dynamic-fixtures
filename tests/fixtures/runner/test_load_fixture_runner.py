from unittest import TestCase

import mock

from dynamic_fixtures.fixtures.exceptions import FixtureNotFound, \
    MultipleFixturesFound
from dynamic_fixtures.fixtures.loader import Graph
from dynamic_fixtures.fixtures.runner import LoadFixtureRunner
from tests.mixins import MockTestCaseMixin


class LoadFixtureRunnerTestCase(MockTestCaseMixin, TestCase):

    def setUp(self):
        try:
            self.loader_mock = self.setup_mock(
                'dynamic_fixtures.fixtures.runner.Loader')
            self.graph_mock = self.setup_mock(
                'dynamic_fixtures.fixtures.runner.Graph')
        except AttributeError:
            # Python 3.4.2 breaks on copying the __module__ when not available
            # on the mocked item.
            print(mock.__version__)

    def test_init(self):
        """
        Case: The runner get initialized
        Expected: The Loader get instantiated and the fixtures get loaded from
                  disc
        """
        LoadFixtureRunner()

        self.loader_mock.assert_called_once_with()
        self.loader_mock.return_value.load_disk.assert_called_once_with()

    def test_graph(self):
        """
        Case: The graph get requested
        Expected: The graph get instantiated once and filled with dependecie
                  data from the Loader
        """
        loader = LoadFixtureRunner()

        fixture_mock = mock.MagicMock()
        fixture_mock.dependencies = ['b', 'c']

        self.loader_mock.return_value.disk_fixtures = {
            'a': fixture_mock,
            'b': mock.MagicMock(),
            'c': mock.MagicMock()
        }

        self.assertFalse(self.graph_mock.called)
        graph = loader.graph
        self.assertIsInstance(graph, Graph)
        self.graph_mock.assert_called_once_with()
        self.graph_mock.return_value.add_node.assert_has_calls([
            mock.call('a'),
            mock.call('b'),
            mock.call('c')
        ], any_order=True)
        self.graph_mock.return_value.add_dependency.assert_has_calls([
            mock.call('a', 'b'),
            mock.call('a', 'c')
        ])
        # Retrieve graph for the 2nd time.
        graph = loader.graph
        self.assertIsInstance(graph, Graph)
        # Should not be instantiated again.
        self.assertEqual(self.graph_mock.call_count, 1)

    def test_get_app_nodes(self):
        """
        Case: Get filtered app nodes
        Expected: Only app nodes which from given app get returned
        """
        runner = LoadFixtureRunner()

        graph = self.graph_mock()
        graph.nodes = [
            ('app_one', 'foo'),
            ('app_one', 'bar'),
            ('app_two', 'foo'),
        ]
        runner._graph = graph

        app_nodes = runner.get_app_nodes('app_one')
        self.assertListEqual(
            app_nodes,
            [
                ('app_one', 'foo'),
                ('app_one', 'bar'),
            ]
        )

    def test_get_fixture_nodes(self):
        """
        Case: Fixture nodes get requested
        Expected: Only nodes starting with the given fixture name get returned
        """

        runner = LoadFixtureRunner()
        runner.get_app_nodes = mock.MagicMock(return_value=[
            ('app_one', '0001_my_fixture'),
            ('app_one', '0002_my_other_fixture'),
            ('app_one', '0003_my_other_fixture'),
        ])

        result = runner.get_fixture_node(app_label='app_one',
                                         fixture_prefix='0001')
        self.assertListEqual(result, [('app_one', '0001_my_fixture')])
        runner.get_app_nodes.assert_called_once_with(app_label='app_one')

    def test_get_fixture_nodes_none_returned(self):
        """
        Case: Fixture nodes get requested but none matches
        Expected: An error get raised
        """
        runner = LoadFixtureRunner()
        runner.get_app_nodes = mock.MagicMock(return_value=[
            ('app_one', '0001_my_fixture'),
            ('app_one', '0002_my_other_fixture'),
            ('app_one', '0003_my_other_fixture'),
        ])

        with self.assertRaises(FixtureNotFound):
            runner.get_fixture_node(app_label='app_one',
                                    fixture_prefix='0006')

    def test_get_fixture_nodes_multiple_returned(self):
        """
        Case: Fixture nodes get requested but multiple matches
        Expected: An error get raised
        """
        runner = LoadFixtureRunner()
        runner.get_app_nodes = mock.MagicMock(return_value=[
            ('app_one', '0001_my_fixture'),
            ('app_one', '0001_my_other_fixture'),
            ('app_one', '0003_my_other_fixture'),
        ])

        with self.assertRaises(MultipleFixturesFound):
            runner.get_fixture_node(app_label='app_one',
                                    fixture_prefix='0001')

    def test_load_fixtures(self):
        """
        Case: Fixtures get loaded
        Expected: For every fixture the load method get called
        """

        runner = LoadFixtureRunner()
        runner._graph = self.graph_mock()
        runner._graph.resolve_node.return_value = [
            ('app_one', '0001_my_fixture'),
            ('app_one', '0002_my_other_fixture'),
            ('app_two', '0001_my_other_fixture'),
        ]
        runner.loader = self.loader_mock()
        runner.loader.disk_fixtures = {
            ('app_one', '0001_my_fixture'): mock.MagicMock(),
            ('app_one', '0002_my_other_fixture'): mock.MagicMock(),
            ('app_two', '0001_my_other_fixture'): mock.MagicMock()
        }

        call_back = mock.Mock(return_value=None)
        runner.load_fixtures(progress_callback=call_back)

        runner.graph.resolve_node.assert_called_once_with()
        for fixture_mock in runner.loader.disk_fixtures.values():
            fixture_mock.load.assert_called_once_with()

        call_back.assert_has_calls([
            mock.call('load_start', ('app_one', '0001_my_fixture')),
            mock.call('load_success', ('app_one', '0001_my_fixture')),
            mock.call('load_start', ('app_one', '0002_my_other_fixture')),
            mock.call('load_success', ('app_one', '0002_my_other_fixture')),
            mock.call('load_start', ('app_two', '0001_my_other_fixture')),
            mock.call('load_success', ('app_two', '0001_my_other_fixture'))
        ])

    def load_fixtures_with_given_nodes(self):
        """
        Case: Load fixtures get called with a given list of nodes
        Expected: resolve_nodes method get called with the list of nodes
        """

        runner = LoadFixtureRunner()
        runner._graph = self.graph_mock()
        runner._graph.resolve_nodes.return_value = [
            ('app_one', '0001_my_fixture'),
            ('app_one', '0002_my_other_fixture'),
        ]
        runner.loader = self.loader_mock()
        runner.loader.disk_fixtures = {
            ('app_one', '0001_my_fixture'): mock.MagicMock(),
            ('app_one', '0002_my_other_fixture'): mock.MagicMock(),
            ('app_two', '0001_my_other_fixture'): mock.MagicMock()
        }

        runner.load_fixtures(nodes=[('app_one', '0001_my_fixture'),
                                    ('app_one', '0002_my_other_fixture')])

        runner.graph.resolve_nodes.assert_called_once_with(
            ('app_one', '0001_my_fixture'),
            ('app_one', '0002_my_other_fixture')
        )
        runner.loader.disk_fixtures[
            ('app_one', '0001_my_fixture')].load.assert_called_once_with()
        runner.loader.disk_fixtures[
            ('app_one', '0001_my_fixture')].load.assert_called_once_with()
        self.assertFalse(runner.loader.disk_fixtures[
                             ('app_one', '0001_my_fixture')].load.called)
