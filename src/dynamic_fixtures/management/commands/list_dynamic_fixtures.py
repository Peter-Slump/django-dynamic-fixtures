from importlib import import_module

from django.apps import apps
from django.core.management.base import BaseCommand

from dynamic_fixtures.fixtures.loader import Loader as OriginLoader
from dynamic_fixtures.fixtures.runner import LoadFixtureRunner as OriginLoadFixtureRunner


class Loader(OriginLoader):
    def load_disk(self):

        self.disk_fixtures = {}

        app_count = 0
        for app_config in apps.get_app_configs():
            app_count += 1
            if app_config.models_module is None:
                print("Skip %s because it has no models" % app_config)
                continue

            self.handle_app_config(app_config=app_config)

        print("\nSearched %i apps." % app_count)

    def handle_app_config(self, app_config):

        # Get the fixtures module directory
        module_name = self.fixtures_module(app_config.label)

        directory = self.get_module_directory(module_name=module_name)

        if directory is None:
            return

        fixture_names = self.get_fixture_files(directory=directory)

        # Load them
        for fixture_name in fixture_names:
            fixture_module_name="%s.%s" % (module_name, fixture_name)
            try:
                fixture_module = import_module(fixture_module_name)
            except Exception as err:
                print("Error with fixture %s: %s" % (fixture_module_name, err))
                continue

            if not hasattr(fixture_module, "Fixture"):
                print("Fixture %s in app %s has no Fixture class, skip." % (fixture_name, app_config.label))
                continue

            self.disk_fixtures[app_config.label, fixture_name] = fixture_module.Fixture(fixture_name, app_config.label)


class LoadFixtureRunner(OriginLoadFixtureRunner):
    def __init__(self):
        self.loader = Loader()
        self.loader.load_disk()
        self._graph = None


class Command(BaseCommand):

    help_text = 'List all dynamic fixtures.'

    def handle(self, *args, **options):
        print()
        print("_"*79)
        print("Discovery all dynamic fixtures...\n")

        runner = LoadFixtureRunner()

        plan = runner.graph.resolve_node()

        print()
        print("_"*79)
        print("All found dynamic fixtures which would be processed in that order:\n")

        fixtures_count = 0
        for node in plan:
            print(" * %-25s" % node[1], end=" ", flush=True)
            obj = runner.loader.disk_fixtures[node]
            print(obj)
            fixtures_count += 1

        print("\nFound %i dynamic fixtures." % fixtures_count)