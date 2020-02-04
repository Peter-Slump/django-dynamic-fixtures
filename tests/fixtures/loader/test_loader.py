import os
import sys
from unittest import mock

from django.test.testcases import TestCase
from django.test.utils import override_settings

from dynamic_fixtures.fixtures.loader import Loader

# Make sure the test apps can be imported
sys.path.append("{}/apps".format(os.path.dirname(os.path.abspath(__file__))))


@override_settings(INSTALLED_APPS=["app_one", "app_two"])
class FixturesLoaderTestCase(TestCase):
    def setUp(self):
        self.loader = Loader()

    def test_load_app(self):
        """
        Case: Fixture modules get loaded
        Expected: The loader contains a dict with the loaded fixtures
        """
        self.loader.load_disk()
        self.assertDictEqual(
            self.loader.disk_fixtures,
            {
                ("app_one", "001_load_some_data"): mock.ANY,
                ("app_one", "002_load_other_data"): mock.ANY,
                ("app_two", "001_load_some_data"): mock.ANY,
            },
        )

        from dynamic_fixtures.fixtures.basefixture import BaseFixture

        for key, fixture in self.loader.disk_fixtures.items():
            self.assertEqual(key[0], fixture._app_label)
            self.assertEqual(key[1], fixture._name)
            self.assertIsInstance(fixture, BaseFixture)

    @override_settings(INSTALLED_APPS=["app_broken_fixture"])
    @mock.patch("dynamic_fixtures.fixtures.loader.logger")
    def test_no_fixture_class(self, logger_mock):
        """
        Case: A app with a fixture file without fixture class get loaded
        Expected: An error is logged that the fixture class is not available.
        """
        self.loader.load_disk()

        self.assertEqual(
            logger_mock.error.mock_calls,
            [
                mock.call(
                    "Fixture {} in app {} has no Fixture class".format(
                        "003_empty_fixture", "app_broken_fixture"
                    )
                )
            ],
        )

    @override_settings(INSTALLED_APPS=["app_wrong_fixture_class"])
    @mock.patch("dynamic_fixtures.fixtures.loader.logger")
    def test_wrong_fixture_class_name(self, logger_mock):
        """
        Case: An app get loaded with a fixture file containing a wrongly named
              fixture class.
        Expected: An error is logged that the fixture class is not available.
        """
        self.loader.load_disk()

        self.assertEqual(
            logger_mock.error.mock_calls,
            [
                mock.call(
                    "Fixture {} in app {} has no Fixture class".format(
                        "003_wrong_fixture_class", "app_wrong_fixture_class"
                    )
                )
            ],
        )

    @override_settings(INSTALLED_APPS=["app_no_fixtures"])
    def test_no_fixture(self):
        """
        Case: An app get loaded with a fixture file containing a wrongly named
              fixture class.
        Expected: An error get raised that the fixture class is not available.
        """
        self.loader.load_disk()
        self.assertDictEqual(self.loader.disk_fixtures, {})
