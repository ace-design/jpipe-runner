"""
jpipe_runner.runtime
~~~~~~~~~~~~~~~~~~~~

This module contains the runtimes that can be used by jPipe Runner.
"""

from ast import literal_eval
from copy import deepcopy
from typing import Any, Iterable, Optional, Tuple

from jpipe_runner.exceptions import RuntimeException


class PythonRuntime:
    """The default lightweight built-in Python runtime."""

    def __init__(self,
                 libraries: Optional[Iterable[str]] = None,
                 variables: Optional[Iterable[Tuple[str, str]]] = None,
                 ):
        self._sandbox_globals = {
            "__builtins__": __builtins__,
        }
        self._sandbox_locals = {}

        if libraries:
            for lib in libraries:
                self.run_file(lib)
        if variables:
            for k, v in variables:
                self.set_variable(k, v)

    def copy(self):
        return deepcopy(self)

    def run_code(self, code: str) -> None:
        try:
            exec(code,
                 self._sandbox_globals,
                 self._sandbox_locals)
        except Exception as e:
            raise RuntimeException(e)

    def run_file(self, filename: str) -> None:
        with open(filename, encoding='utf-8') as f:
            content = f.read()
        self.run_code(code=content)

    def import_module(self, name: str) -> None:
        module = __import__(name)
        self.set_variable(name, module)

    def call_function(self, name: str, *args, **kwargs) -> Any:
        fn = self.get_variable(name)
        return fn(*args, **kwargs)

    def has_variable(self, name: str) -> bool:
        return (name in self._sandbox_locals) or \
            (name in self._sandbox_globals)

    def get_variable(self, name: str) -> Any:
        if name in self._sandbox_locals:
            return self._sandbox_locals[name]
        elif name in self._sandbox_globals:
            return self._sandbox_globals[name]
        raise RuntimeException(
            f"'{name}' is not defined in the runtime")

    def set_variable(self, name: str, value: Any) -> None:
        self._sandbox_globals[name] = value

    def set_variable_literal(self, name: str, literal: str) -> None:
        self.set_variable(name, literal_eval(literal))


def __test_python_runtime():
    runtime = PythonRuntime()

    runtime.run_code("""
# x = 123
def len_of_x():
    return len(x)
""")

    runtime.set_variable('x', [1, 2, 3])
    assert runtime.call_function('len_of_x') == 3

    runtime.set_variable_literal('x', '(1,5,9,3,7)')
    assert runtime.call_function('len_of_x') == 5

    runtime.set_variable_literal('x', '"(1,5,9,3,7)"')
    assert runtime.call_function('len_of_x') == 11

    assert not runtime.has_variable('hello')
    runtime.run_code("""
def hello():
    print(x)
""")
    assert runtime.has_variable('hello')
    assert runtime.call_function('hello') is None

    runtime.import_module('os')
    runtime.run_code("""print(os.curdir)""")


if __name__ == '__main__':
    __test_python_runtime()
