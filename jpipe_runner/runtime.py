"""
jpipe_runner.runtime
~~~~~~~~~~~~~~~~~~~~

This module contains the runtimes that can be used by jPipe Runner.
"""

import importlib.util
import os
from ast import literal_eval
from typing import Any, Iterable, Optional, Tuple

from jpipe_runner.exceptions import RuntimeException


class PythonRuntime:
    """The default lightweight built-in Python runtime."""

    def __init__(self,
                 libraries: Optional[Iterable[str]] = None,
                 variables: Optional[Iterable[Tuple[str, str]]] = None,
                 ):
        self._modules = []
        self.load_files(libraries or [])

        for k, v in variables or []:
            self.set_variable(k, v)

    def load_files(self, file_paths: Iterable[str]):
        for file_path in file_paths:
            self._import_file(file_path)

    def _import_file(self, file_path: str) -> None:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        module_name, _ = os.path.splitext(
            os.path.basename(file_path))
        spec = importlib.util. \
            spec_from_file_location(module_name, file_path)
        module = importlib.util. \
            module_from_spec(spec)
        spec.loader.exec_module(module)

        self._modules.append(module)

    def _find_module_by_attr(self, name: str) -> Any:
        for module in self._modules:
            if name in dir(module):
                return module
        raise RuntimeException(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getattr__(self, name):
        module = self._find_module_by_attr(name)
        return getattr(module, name)

    def call_function(self, name: str, *args, **kwargs) -> Any:
        return self.__getattr__(name)(*args, **kwargs)

    def set_variable(self, name: str, value: Any) -> None:
        module = self._find_module_by_attr(name)
        return setattr(module, name, value)

    def set_variable_literal(self, name: str, literal: str) -> None:
        self.set_variable(name, literal_eval(literal))
