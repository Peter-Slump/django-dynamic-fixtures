import time

from django.db import transaction

from dynamic_fixtures.fixtures.exceptions import (
    MultipleFixturesFound,
    FixtureNotFound,
    DryRun)
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
        nodes = [
            node for node in app_nodes if node[1].startswith(fixture_prefix)
            ]

        if len(nodes) > 1:
            raise MultipleFixturesFound(
                "The following fixtures with prefix '%s' are found in app '%s'"
                ": %s" % (
                    fixture_prefix, app_label, ', '.join(
                        [node[1] for node in nodes]
                    )
                )
            )
        elif len(nodes) == 0:
            raise FixtureNotFound("Fixture with prefix '%s' not found in app "
                                  "'%s'" % (fixture_prefix, app_label))
        return nodes

    def load_fixtures(self, nodes=None, progress_callback=None, dry_run=False):
        """Load all fixtures for given nodes.

        If no nodes are given all fixtures will be loaded.
        :param list nodes: list of nodes to be loaded.
        :param callable progress_callback: Callback which will be called while
                                           handling the nodes.
        """

        if progress_callback and not callable(progress_callback):
            raise Exception('Callback should be callable')

        plan = self.get_plan(nodes=nodes)

        try:
            with transaction.atomic():
                self.load_plan(plan=plan, progress_callback=progress_callback)
                if dry_run:
                    raise DryRun
        except DryRun:
            # Dry-run to get the atomic transaction rolled back
            pass

        return len(plan)

    def load_plan(self, plan, progress_callback):
        # Load every fixture in the plan.
        for node in plan:
            if progress_callback:
                progress_callback('load_start', node)

            start = time.time()
            self.loader.disk_fixtures[node].load()
            if progress_callback:
                progress_callback('load_success', node, time.time() - start)

    def get_plan(self, nodes=None):
        """
        Retrieve a plan, e.g. a list of fixtures to be loaded sorted on
        dependency.

        :param list nodes: list of nodes to be loaded.
        :return:
        """
        if nodes:
            plan = self.graph.resolve_nodes(nodes)
        else:
            plan = self.graph.resolve_node()

        return plan
