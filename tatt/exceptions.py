
class ConfigError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class DoesntExistError(Exception):
    pass


class NotAvailable(Exception):
    pass


class DependencyRequired(Exception):
    pass


class FormatError(Exception):
    pass
