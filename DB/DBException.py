

class DBExceptions(Exception):
    """Base class for my database Exceptions in this module."""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

    def my_exception(self, message):
        raise Exception(message)
