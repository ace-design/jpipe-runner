"""
jpipe_runner.exceptions
~~~~~~~~~~~~~~~~~~~~~~~

This module contains the set of jPipe Runner's exceptions.
"""


class RunnerException(Exception):
    """There was an ambiguous exception that occurred while running the runner."""


class SyntaxException(RunnerException):
    """A syntax error occurred."""


class UnsupportedException(RunnerException):
    """An unsupported error occurred."""


class NotFoundException(RunnerException):
    """A not found error occurred."""
