import os

from importlib import import_module

from django.apps import apps

from dynamic_fixtures.fixtures.exceptions import BadFixtureError

FIXTURES_MODULE_NAME = 'fixtures'


class Loader(object):

    def __init__(self):
        self.disk_fixtures = None

    @classmethod
    def fixtures_module(cls, app_label):
        app_package_name = apps.get_app_config(app_label).name
        return '%s.%s' % (app_package_name, FIXTURES_MODULE_NAME)

    def load_disk(self):

        self.disk_fixtures = {}

        for app_config in apps.get_app_configs():
            # No models no need for fixtures
            if app_config.models_module is None:
                continue

            self.handle_app_config(app_config=app_config)

    def handle_app_config(self, app_config):

        # Get the fixtures module directory
        module_name = self.fixtures_module(app_config.label)

        directory = self.get_module_directory(module_name=module_name)

        if directory is None:
            return

        fixture_names = self.get_fixture_files(directory=directory)

        # Load them
        for fixture_name in fixture_names:
            fixture_module = import_module("%s.%s" % (module_name, fixture_name))
            if not hasattr(fixture_module, "Fixture"):
                raise BadFixtureError(
                    "Fixture %s in app %s has no Fixture class" % (fixture_name, app_config.label))
            self.disk_fixtures[app_config.label, fixture_name] = fixture_module.Fixture(fixture_name, app_config.label)

    @staticmethod
    def get_fixture_files(directory):
        # Scan for .py files
        fixture_names = set()
        for name in os.listdir(directory):
            if name.endswith(".py"):
                import_name = name.rsplit(".", 1)[0]
                if import_name[0] not in "_.~":
                    fixture_names.add(import_name)
        return fixture_names

    @staticmethod
    def get_module_directory(module_name):
        try:
            module = import_module(module_name)
        except ImportError as e:
            # I hate doing this, but I don't want to squash other import errors.
            # Might be better to try a directory check directly.
            if "No module named" in str(e) and FIXTURES_MODULE_NAME in str(e):
                return
            raise

        try:
            directory = os.path.dirname(module.__file__)
        except AttributeError:
            # No __file__ available for module
            return

        return directory


class Graph(object):
    """A dependency graph
    """

    def __init__(self):
        self._nodes = {}

    @property
    def nodes(self):
        return self._nodes

    def add_node(self, node):
        self._nodes.setdefault(node, list())

    def add_dependency(self, node, dependency):
        if node not in self._nodes:
            raise KeyError('Node %s not set', str(node))
        if dependency not in self._nodes:
            raise KeyError('Dependency "%s" required for "%s" but is not set.', str(dependency), str(node))
        self._nodes[node].append(dependency)

    def __iter__(self):
        for resolved_node in self.resolve_node():
            yield resolved_node

    def resolve_nodes(self, nodes):
        """
        Resolve a given set of nodes.

        Dependencies of the nodes, even if they are not in the given list will
        also be resolved!

        :param list nodes: List of nodes to be resolved
        :return: A list of resolved nodes
        """
        if not nodes:
            return []
        resolved = []
        for node in nodes:
            if node in resolved:
                continue
            self.resolve_node(node, resolved)
        return resolved

    def resolve_node(self, node=None, resolved=None, seen=None):
        """
        Resolve a single node or all when node is omitted.
        """
        if seen is None:
            seen = []
        if resolved is None:
            resolved = []
        if node is None:
            dependencies = sorted(self._nodes.keys())
        else:
            dependencies = self._nodes[node]
            seen.append(node)
        for dependency in dependencies:
            if dependency in resolved:
                continue
            if dependency in seen:
                raise Exception('Circular dependency %s > %s', str(node),
                                str(dependency))
            self.resolve_node(dependency, resolved, seen)
        if node is not None:
            resolved.append(node)
        return resolved
