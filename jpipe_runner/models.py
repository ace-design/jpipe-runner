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
    action: Optional[Callable] = lambda: True


@dataclass(order=True, unsafe_hash=True)
class SupportDef:
    left: str
    right: str


@dataclass(order=True)
class JustificationDef:
    variables: Optional[list[VariableDef]]
    supports: Optional[list[SupportDef]]


@dataclass(order=True)
class CompositionDef:
    compositions: Optional[list[Any]]


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
