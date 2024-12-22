"""
jpipe_runner.runtime
~~~~~~~~~~~~~~~~~~~~

This module contains the runtimes that can be used by jPipe Runner.
"""


class BaseRuntime:
    pass


class PythonRuntime(BaseRuntime):
    """PythonRuntime is the default built-in python runtime"""
    pass


class JSRuntime(BaseRuntime):
    pass
