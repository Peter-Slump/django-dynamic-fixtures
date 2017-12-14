from django.core.management.base import BaseCommand

from dynamic_fixtures.fixtures.runner import LoadFixtureRunner


class Command(BaseCommand):

    help_text = 'Load fixtures while keeping dependencies in mind.'
    args = '[app_label] [fixture_name]'

    def add_arguments(self, parser):
        parser.add_argument('app_label', default=None, nargs='?', type=str)
        parser.add_argument('fixture_name', default=None, nargs='?', type=str)

    def handle(self, *args, **options):
        runner = LoadFixtureRunner()

        if len(args) == 1:
            fixture_name = None
            app_label, = args
        elif len(args) == 2:
            app_label, fixture_name = args
        else:
            app_label = options.get('app_label')
            fixture_name = options.get('fixture_name')

        if app_label is None:
            nodes = None
        elif fixture_name is None:
            nodes = runner.get_app_nodes(app_label=app_label)
        else:
            nodes = runner.get_fixture_node(app_label=app_label,
                                            fixture_prefix=fixture_name)

        fixture_count = runner.load_fixtures(
            nodes=nodes,
            progress_callback=self.progress_callback
        )
        
        self.stdout.write('Loaded {} fixtures'.format(fixture_count))

    def progress_callback(self, action, node):
        if action == 'load_start':
            self.stdout.write('Loading fixture {}.{}...'.format(*node),
                              ending='')
            self.stdout.flush()
        elif action == 'load_success':
            self.stdout.write('SUCCESS')
