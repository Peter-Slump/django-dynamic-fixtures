from unittest import TestCase

from dynamic_fixtures.fixtures.basefixture import BaseFixture


class BaseFixtureTestCase(TestCase):

    def test_load_not_implemented(self):
        """
        Case: load is not implemented
        Expected: Error get raised
        """
        fixture = BaseFixture('Name', 'Module')
        with self.assertRaises(NotImplementedError):
            fixture.load()
