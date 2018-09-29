class BadFixtureError(Exception):
    pass


class MultipleFixturesFound(Exception):
    pass


class FixtureNotFound(Exception):
    pass


class DryRun(Exception):
    pass
