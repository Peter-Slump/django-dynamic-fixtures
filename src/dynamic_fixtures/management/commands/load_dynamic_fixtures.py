from django.core.management.base import BaseCommand

from dynamic_fixtures.fixtures.runner import LoadFixtureRunner


class Command(BaseCommand):

    help_text = 'Load fixtures while keeping dependencies in mind.'
    args = '[app_label] [fixture_name]'

    def handle(self, *args, **options):
        runner = LoadFixtureRunner()
        nodes = None
        if len(args) == 1:
            nodes = runner.get_app_nodes(app_label=args[0])
        elif len(args) == 2:
            nodes = runner.get_fixture_node(app_label=args[0],
                                            fixture_prefix=args[1])

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
