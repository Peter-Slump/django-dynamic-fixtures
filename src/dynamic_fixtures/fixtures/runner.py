from dynamic_fixtures.fixtures.exceptions import (
    MultipleFixturesFound,
    FixtureNotFound
)
from dynamic_fixtures.fixtures.loader import Loader, Graph


class LoadFixtureRunner(object):

    def __init__(self):
        self.loader = Loader()
        self.loader.load_disk()

        self._graph = None

    @property
    def graph(self):
        if not self._graph:
            self.init_graph()
        return self._graph

    def init_graph(self):
        """
        Initialize graph
        Load all nodes and set dependencies.

        To avoid errors about missing nodes all nodes get loaded first before
        setting the dependencies.
        """
        self._graph = Graph()

        # First add all nodes
        for key in self.loader.disk_fixtures.keys():
            self.graph.add_node(key)

        # Then set dependencies
        for key, fixture in self.loader.disk_fixtures.items():
            for dependency in fixture.dependencies:
                self.graph.add_dependency(key, dependency)

    def get_app_nodes(self, app_label):
        """
        Get all nodes for given app
        :param str app_label: app label
        :rtype: list
        """
        return [node for node in self.graph.nodes if node[0] == app_label]

    def get_fixture_node(self, app_label, fixture_prefix):
        """
        Get all fixtures in given app with given prefix.
        :param str app_label: App label
        :param str fixture_prefix: first part of the fixture name
        :return: list of found fixtures.
        """
        app_nodes = self.get_app_nodes(app_label=app_label)
        nodes = [node for node in app_nodes if node[1].startswith(fixture_prefix)]

        if len(nodes) > 1:
            raise MultipleFixturesFound("The following fixtures with prefix "
                                        "'%s' are found in app '%s': %s" %
                                        (fixture_prefix, app_label,
                                        ', '.join([node[1] for node in nodes])))
        elif len(nodes) == 0:
            raise FixtureNotFound("Fixture with prefix '%s' not found in app "
                                  "'%s'" % (fixture_prefix, app_label))
        return nodes

    def load_fixtures(self, nodes=None, progress_callback=None):
        """Load all fixtures for given nodes.

        If no nodes are given all fixtures will be loaded.
        :param list nodes: list of nodes to be loaded.
        :param callable progress_callback: Callback which will be called while
                                           handling the nodes.
        """
        
        fixture_count = 0

        if progress_callback and not callable(progress_callback):
            raise Exception('Callback should be callable')

        # First retrieve a plan, e.g. a list of fixtures to be loaded sorted on
        # dependency.
        if nodes:
            plan = self.graph.resolve_nodes(nodes)
        else:
            plan = self.graph.resolve_node()

        # Load every fixture in the plan.
        for node in plan:
            if progress_callback:
                progress_callback('load_start', node)
            self.loader.disk_fixtures[node].load()
            if progress_callback:
                progress_callback('load_success', node)
            fixture_count += 1
        
        return fixture_count
