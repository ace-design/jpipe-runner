"""
jpipe_runner.definitions
~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the definitions of Justification Diagram.
"""

from enum import Enum
from pprint import pformat
from typing import Any, Optional


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


class LoadStmt:
    def __init__(self,
                 path: str,
                 ):
        self.path = path

    def __repr__(self):
        return f"<LoadStmt path={repr(self.path)}>"


class ClassDef:
    def __init__(self,
                 class_type: ClassType,
                 name: str,
                 pattern: Optional[str] = None,
                 ):
        # justification / pattern / composition
        self.class_type = class_type
        self.name = name
        self.pattern = pattern
        self.body = None

    def __repr__(self):
        return f"<ClassDef type={self.class_type} name={self.name} implements={self.pattern} body={self.body}>"


class VariableDef:
    def __init__(self,
                 var_type: VariableType,
                 name: str,
                 description: str,
                 ):
        self.var_type = var_type
        self.name = name
        self.description = description
        # TODO: mapped action function
        self.action = lambda: True

    def __repr__(self):
        return f"<VariableDef type={self.var_type} name={self.name} desc={repr(self.description)}>"


class SupportDef:
    def __init__(self,
                 left: str,
                 right: str,
                 ):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"<SupportDef {self.left} -> {self.right}>"


class JustificationDef:
    def __init__(self,
                 variables: Optional[list[VariableDef]] = None,
                 supports: Optional[list[SupportDef]] = None,
                 ):
        if variables is None:
            variables = []
        if supports is None:
            supports = []
        self.variables = variables
        self.supports = supports

    def __repr__(self):
        return f"<JustificationDef vars={pformat(self.variables)} supports={pformat(self.supports)}>"


class CompositionDef:
    def __init__(self,
                 compositions: Optional[list[Any]] = None,
                 ):
        if compositions is None:
            compositions = []
        self.compositions = compositions

    def __repr__(self):
        return f"<CompositionDef compositions={pformat(self.compositions)}>"
