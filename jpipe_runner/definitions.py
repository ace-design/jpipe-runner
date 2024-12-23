"""
jpipe_runner.definitions
~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the definitions of Justification Diagram.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional, Union


class ClassType(Enum):
    """justification / pattern / composition"""
    JUSTIFICATION = "justification"
    PATTERN = "pattern"
    COMPOSITION = "composition"


class VariableType(Enum):
    """evidence / strategy / sub-conclusion / conclusion / @support"""
    EVIDENCE = "evidence"
    STRATEGY = "strategy"
    SUB_CONCLUSION = "sub-conclusion"
    CONCLUSION = "conclusion"
    SUPPORT = "@support"


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
