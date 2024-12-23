"""
jpipe_runner.models
~~~~~~~~~~~~~~~~~~~

This module contains the model definitions of Justification Diagram.
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional

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


@dataclass(order=True, frozen=True)
class SupportDef:
    left: str
    right: str


@dataclass(order=True)
class JustificationDef:
    variables: Optional[set[VariableDef]] = None
    supports: Optional[set[SupportDef]] = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = set()
        if self.supports is None:
            self.supports = set()


@dataclass(order=True)
class CompositionDef:
    compositions: Optional[set[Any]] = None

    def __post_init__(self):
        if self.compositions is None:
            self.compositions = set()


@dataclass(order=True)
class LoadStmt:
    path: str


@dataclass(order=True)
class ClassDef:
    class_type: ClassType
    name: str
    pattern: Optional[str] = None
    body: JustificationDef | CompositionDef = None


@dataclass(order=True)
class ModelDef:
    load_stmts: list[LoadStmt]
    class_defs: list[ClassDef]
