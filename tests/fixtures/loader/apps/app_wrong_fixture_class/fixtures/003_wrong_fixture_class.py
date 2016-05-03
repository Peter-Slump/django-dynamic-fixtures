from factory_boy_fixtures.fixtures.basefixture import BaseFixture


# Will not be loaded
class WrongFixtureClass(BaseFixture):
    pass