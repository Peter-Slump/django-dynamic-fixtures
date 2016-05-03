import sys
import os

from django.test.testcases import TestCase
from django.test.utils import override_settings

import mock

from factory_boy_fixtures.fixtures.exceptions import BadFixtureError
from factory_boy_fixtures.fixtures.loader import Loader

# Make sure the test apps can be imported
sys.path.append('{}/apps'.format(os.path.dirname(os.path.abspath(__file__))))


@override_settings(INSTALLED_APPS=['app_one', 'app_two'])
class FixturesLoaderTestCase(TestCase):

    def setUp(self):
        self.loader = Loader()

    def test_load_app(self):
        """
        Case: Fixture modules get loaded
        Expected: The loader contains a dict with the loaded fixtures
        """
        self.loader.load_disk()
        self.assertDictEqual(self.loader.disk_fixtures, {
            ('app_one', '001_load_some_data'): mock.ANY,
            ('app_one', '002_load_other_data'): mock.ANY,
            ('app_two', '001_load_some_data'): mock.ANY,
        })

        from factory_boy_fixtures.fixtures.basefixture import BaseFixture
        for key, fixture in self.loader.disk_fixtures.items():
            self.assertEqual(key[0], fixture._app_label)
            self.assertEqual(key[1], fixture._name)
            self.assertIsInstance(fixture, BaseFixture)

    @override_settings(INSTALLED_APPS=['app_broken_fixture'])
    def test_no_fixture_class(self):
        """
        Case: A app with a fixture file without fixture class get loaded
        Expected: An error get raised that the fixture class is not available.
        """
        with self.assertRaises(BadFixtureError):
            self.loader.load_disk()

    @override_settings(INSTALLED_APPS=['app_wrong_fixture_class'])
    def test_wrong_fixture_class_name(self):
        """
        Case: An app get loaded with a fixture file containing a wrongly named
              fixture class.
        Expected: An error get raised that the fixture class is not available.
        """
        with self.assertRaises(BadFixtureError):
            self.loader.load_disk()

    @override_settings(INSTALLED_APPS=['app_no_fixtures'])
    def test_no_fixture(self):
        """
        Case: An app get loaded with a fixture file containing a wrongly named
              fixture class.
        Expected: An error get raised that the fixture class is not available.
        """
        self.loader.load_disk()
        self.assertDictEqual(self.loader.disk_fixtures, {})