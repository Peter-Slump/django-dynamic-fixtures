import os
import copy

from importlib import import_module

from django.apps import apps

from factory_boy_fixtures.fixtures.exceptions import BadFixtureError

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

            # Get the fixtures module diectory
            module_name = self.fixtures_module(app_config.label)
            try:
                module = import_module(module_name)
            except ImportError as e:
                # I hate doing this, but I don't want to squash other import errors.
                # Might be better to try a directory check directly.
                if "No module named" in str(e) and FIXTURES_MODULE_NAME in str(e):
                    continue
                raise
            directory = os.path.dirname(module.__file__)
            # Scan for .py files
            fixture_names = set()
            for name in os.listdir(directory):
                if name.endswith(".py"):
                    import_name = name.rsplit(".", 1)[0]
                    if import_name[0] not in "_.~":
                        fixture_names.add(import_name)
            # Load them
            for fixture_name in fixture_names:
                fixture_module = import_module("%s.%s" % (module_name, fixture_name))
                if not hasattr(fixture_module, "Fixture"):
                    raise BadFixtureError(
                        "Fixture %s in app %s has no Fixture class" % (fixture_name, app_config.label))
                self.disk_fixtures[app_config.label, fixture_name] = fixture_module.Fixture(fixture_name, app_config.label)


class Graph(object):
    """A dependency graph
    """

    def __init__(self):
        self._nodes = {}

    def add_node(self, node):
        self._nodes.setdefault(node, set())

    def add_dependency(self, node, dependency):
        if node not in self._nodes:
            raise KeyError('Node %s not set', str(node))
        if dependency not in self._nodes:
            raise KeyError('Dependency %s not set', str(dependency))
        self._nodes[node].add(dependency)

    def __iter__(self):
        resolved_nodes = []
        for node in self._nodes.items():
            if node in resolved_nodes:
                continue
            for resolved in self.resolve_node(node, resolved_nodes):
                resolved_nodes.append(resolved)
                yield resolved

    def resolve_node(self, node, resolved, seen=None):
        seen = seen or []
        seen.append(node)
        for dependency in self._nodes[node]:
            if dependency in resolved:
                continue
            if dependency in seen:
                raise Exception('Circular dependency %s > %s', str(node), str(dependency))
            yield self.resolve_node(dependency, resolved, seen)
        yield node
