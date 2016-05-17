class BaseFixture(object):

    def __init__(self, name, app_label):
        self._name = name
        self._app_label = app_label

    # Other fixtures which should be loaded first. This should be a list of:
    # ('app_label', 'fixture_name')
    dependencies = []

    def load(self):
        """
        Load the fixtures.
        This method should be overridden to actual load the fixture data.
        :return: A list of created fixture models.
        """
        raise NotImplementedError()