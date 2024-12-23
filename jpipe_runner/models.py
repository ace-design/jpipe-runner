"""
jpipe_runner.models
~~~~~~~~~~~~~~~~~~~

This module contains the model definitions of Justification Diagram.
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional

from jpipe_runner.enums import ClassType, VariableType


@dataclass(order=True)
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
    supports: Optional[set[SupportDef]] = None
    variables: Optional[dict[str, VariableDef]] = None

    def __post_init__(self):
        if self.supports is None:
            self.supports = set()
        if self.variables is None:
            self.variables = dict()


@dataclass(order=True)
class CompositionDef:
    compositions: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.compositions is None:
            self.compositions = dict()


@dataclass(order=True, frozen=True)
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
    load_stmts: Optional[set[LoadStmt]] = None
    class_defs: Optional[dict[str, ClassDef]] = None

    def __post_init__(self):
        if self.load_stmts is None:
            self.load_stmts = set()
        if self.class_defs is None:
            self.class_defs = dict()

    def update(self, model) -> None:
        assert isinstance(model, ModelDef)
        self.load_stmts.update(model.load_stmts)
        self.class_defs.update(model.class_defs)
