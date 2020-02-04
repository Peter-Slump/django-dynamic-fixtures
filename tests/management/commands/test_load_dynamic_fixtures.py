from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from tests.mixins import MockTestCaseMixin


class ManagementCommandLoadDynamicFixturesTestCase(MockTestCaseMixin, TestCase):
    def setUp(self):
        self.fixtures_runner_mock = self.setup_mock(
            "dynamic_fixtures.management.commands.load_dynamic_fixtures"
            ".LoadFixtureRunner"
        )

    def test_service_got_called(self):
        """
        Case: Management command get called
        Expected: Module get initialized and run
        """
        call_command("load_dynamic_fixtures")

        self.fixtures_runner_mock.assert_called_once_with()
        self.assertFalse(self.fixtures_runner_mock.return_value.get_app_nodes.called)

        self.fixtures_runner_mock.return_value.load_fixtures.assert_called_once_with(
            progress_callback=mock.ANY, nodes=None, dry_run=False
        )

    def test_one_argument(self):
        """
        Case: management command is called with one argument (app)
        Expected: the nodes from the app get returned
        """
        call_command("load_dynamic_fixtures", "my_app")

        self.fixtures_runner_mock.assert_called_once_with()
        self.fixtures_runner_mock.return_value.get_app_nodes.assert_called_once_with(
            app_label="my_app"
        )

        self.fixtures_runner_mock.return_value.load_fixtures.assert_called_once_with(
            progress_callback=mock.ANY,
            nodes=self.fixtures_runner_mock.return_value.get_app_nodes.return_value,
            dry_run=False,
        )

    def test_two_arguments(self):
        """
        Case: management command is called with two argument (app, fixture)
        Expected: the nodes from the app get returned
        """
        call_command("load_dynamic_fixtures", "my_app", "0001")

        self.fixtures_runner_mock.assert_called_once_with()
        self.fixtures_runner_mock.return_value.get_fixture_node.assert_called_once_with(
            app_label="my_app", fixture_prefix="0001"
        )

        self.fixtures_runner_mock.return_value.load_fixtures.assert_called_once_with(
            progress_callback=mock.ANY,
            nodes=self.fixtures_runner_mock.return_value.get_fixture_node.return_value,
            dry_run=False,
        )

    def test_app_label_argument(self):
        """
        Case: management command is called with one argument (app)
        Expected: the nodes from the app get returned
        """
        call_command("load_dynamic_fixtures", app_label="my_app")

        self.fixtures_runner_mock.assert_called_once_with()
        self.fixtures_runner_mock.return_value.get_app_nodes.assert_called_once_with(
            app_label="my_app"
        )

        self.fixtures_runner_mock.return_value.load_fixtures.assert_called_once_with(
            progress_callback=mock.ANY,
            nodes=self.fixtures_runner_mock.return_value.get_app_nodes.return_value,
            dry_run=False,
        )

    def test_app_label_and_fixture_prefix_arguments(self):
        """
        Case: management command is called with two argument (app, fixture)
        Expected: the nodes from the app get returned
        """
        call_command("load_dynamic_fixtures", app_label="my_app", fixture_name="0001")

        self.fixtures_runner_mock.assert_called_once_with()
        self.fixtures_runner_mock.return_value.get_fixture_node.assert_called_once_with(
            app_label="my_app", fixture_prefix="0001"
        )

        self.fixtures_runner_mock.return_value.load_fixtures.assert_called_once_with(
            progress_callback=mock.ANY,
            nodes=self.fixtures_runner_mock.return_value.get_fixture_node.return_value,
            dry_run=False,
        )
