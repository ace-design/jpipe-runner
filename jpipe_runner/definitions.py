"""
jpipe_runner.definitions
~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the definitions of Justification Diagram.
"""

from enum import Enum
from typing import Optional


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


class ClassDef:
    def __init__(self,
                 class_type: ClassType,
                 name: str,
                 implements: Optional[str] = None,
                 ):
        # justification / pattern / composition
        self.class_type = class_type
        self.name = name
        self.implements = implements
        self.body = None

    def __repr__(self):
        return f"<ClassDef type={self.class_type} name={self.name} implements={self.implements} body={self.body}>"


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
        return f"<VariableDef type={self.var_type} name={self.name} desc={self.description}>"


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
    def __init__(self):
        # list of VariableDef
        self.variables = []
        # list of SupportDef
        self.supports = []

    def __repr__(self):
        return f"<JustificationDef vars={self.variables} supports={self.supports}>"


class CompositionDef:
    def __init__(self):
        self.compositions = []

    def __repr__(self):
        return f"<CompositionDef {self.compositions}>"
