from django.core.management.base import BaseCommand

from dynamic_fixtures.fixtures.runner import LoadFixtureRunner


class Command(BaseCommand):

    help_text = 'Load fixtures while keeping dependencies in mind.'
    args = '[app_label] [fixture_name]'

    def add_arguments(self, parser):
        parser.add_argument('app_label', default=None, nargs='?', type=str)
        parser.add_argument('fixture_name', default=None, nargs='?', type=str)
        parser.add_argument('--list', action='store_true', dest='list',
                            help='List all available fixtures')
        parser.add_argument('--dry-run', action='store_true', dest='dry_run',
                            help='Don\'t actually load the fixtures.')

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

        if not options.get('list', False):

            fixture_count = runner.load_fixtures(
                nodes=nodes,
                progress_callback=self.progress_callback,
                dry_run=options.get('dry_run', False)
            )

        else:
            plan = runner.get_plan(nodes=nodes)

            self.stdout.write('Discovery all dynamic fixtures...')
            for node in plan:
                self.stdout.write('{}.{}'.format(*node))

            fixture_count = len(plan)

        self.stdout.write('Total of {} fixtures'.format(fixture_count))

        if not options.get('list') and options.get('dry_run'):
            self.stdout.write('Dry-run: all changes are rolled back.')

    def progress_callback(self, action, node, elapsed_time=None):
        """
        Callback to report progress

        :param str action:
        :param list node: app, module
        :param int | None elapsed_time:
        """
        if action == 'load_start':
            self.stdout.write('Loading fixture {}.{}...'.format(*node),
                              ending='')
            self.stdout.flush()
        elif action == 'load_success':
            message = 'SUCCESS'
            if elapsed_time:
                message += ' ({:.03} seconds) '.format(elapsed_time)

            self.stdout.write(message)
