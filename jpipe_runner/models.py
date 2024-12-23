"""
jpipe_runner.models
~~~~~~~~~~~~~~~~~~~

This module contains the model definitions of Justification Diagram.
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional, Union

from jpipe_runner.enums import ClassType, VariableType


@dataclass(order=True, unsafe_hash=True)
class VariableDef:
    var_type: VariableType
    name: str
    description: str

    # TODO: mapped action function
    action: Optional[Callable] = None

    def __post_init__(self):
        if self.action is None:
            self.action = lambda: True


@dataclass(order=True, unsafe_hash=True)
class SupportDef:
    left: str
    right: str


@dataclass(order=True)
class JustificationDef:
    variables: Optional[list[VariableDef]] = None
    supports: Optional[list[SupportDef]] = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = []
        if self.supports is None:
            self.supports = []


@dataclass(order=True)
class CompositionDef:
    compositions: Optional[list[Any]] = None

    def __post_init__(self):
        if self.compositions is None:
            self.compositions = []


@dataclass(order=True)
class LoadStmt:
    path: str


@dataclass(order=True)
class ClassDef:
    class_type: ClassType
    name: str
    pattern: Optional[str] = None
    body: Union[JustificationDef | CompositionDef] = None


@dataclass(order=True)
class ModelDef:
    load_stmts: list[LoadStmt]
    class_defs: list[ClassDef]
