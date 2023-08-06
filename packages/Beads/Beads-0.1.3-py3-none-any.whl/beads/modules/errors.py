class InternalException(BaseException):
    """ Error Base class providing exception management on highest level """
    pass


class ValidationError(InternalException):
    """ Any error that occurs while validating the internal logic of a fine state machine """
    def __init__(self, cause):
        self.cause = cause


class UnsupportedLanguageError(InternalException):
    """ Error indicating that the provided language option is not supported """


class ParsingError(InternalException):
    """ Any error that occurs while trying to parse the provided input """
    def __init__(self, cause):
        self.cause = cause


class ExistingFileError(InternalException):
    """ Error indicating that a file with the same name already exists and the '-re' flag is not set """
