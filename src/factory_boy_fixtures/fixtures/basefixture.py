

class BaseFixture(object):

    def __init__(self, name, app_label):
        self._name = name
        self._app_label = app_label