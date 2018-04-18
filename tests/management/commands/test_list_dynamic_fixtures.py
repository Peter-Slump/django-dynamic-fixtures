import mock
from io import StringIO

from django.test import TestCase, modify_settings
from django.core.management import call_command

from tests.mixins import MockTestCaseMixin


class ManagementCommandLoadDynamicFixturesTestCase(MockTestCaseMixin, TestCase):

    def test_app_one(self):
        APPS=[
            "tests.fixtures.loader.apps.app_one",
        ]
        with modify_settings(INSTALLED_APPS={"append": APPS}):
            with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                call_command('list_dynamic_fixtures')

        output = mock_stdout.getvalue()
        print(output)

        self.assertIn("Searched 8 apps.", output)

        self.assertIn("001_load_some_data", output)
        self.assertIn("002_load_other_data", output)

        self.assertIn("Found 2 dynamic fixtures", output)

    def test_app_wrong_fixture_class(self):
        APPS=[
            "tests.fixtures.loader.apps.app_wrong_fixture_class",
        ]
        with modify_settings(INSTALLED_APPS={"append": APPS}):
            with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                call_command('list_dynamic_fixtures')

        output = mock_stdout.getvalue()
        print(output)

        self.assertIn("Fixture 003_wrong_fixture_class in app app_wrong_fixture_class has no Fixture class, skip.", output)

        self.assertIn("Searched 8 apps.", output)

        self.assertIn("Found 0 dynamic fixtures", output)

    def test_app_broken_fixture_class(self):
        APPS=[
            "tests.fixtures.loader.apps.app_broken_fixture",
        ]
        with modify_settings(INSTALLED_APPS={"append": APPS}):
            with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                call_command('list_dynamic_fixtures')

        output = mock_stdout.getvalue()
        print(output)

        self.assertIn("Fixture 003_empty_fixture in app app_broken_fixture has no Fixture class, skip.", output)

        self.assertIn("Searched 8 apps.", output)

        self.assertIn("Found 0 dynamic fixtures", output)
