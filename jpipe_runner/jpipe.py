"""
jpipe_runner.jpipe
~~~~~~~~~~~~~~~~~~

This module contains the core of jPipe Runner.
"""

from copy import deepcopy

from jpipe_runner.enums import ClassType, VariableType
from jpipe_runner.exceptions import UnsupportedException, InvalidJustificationException
from jpipe_runner.models import ModelDef, JustificationDef
from jpipe_runner.parser import parse_jd_file


class JPipe:

    def __init__(self,
                 model: ModelDef,
                 ):
        self._model = deepcopy(model)
        self._init_model()

    def _init_model(self) -> None:
        if len(self._model.load_stmts) > 0:
            raise UnsupportedException("load statement is not supported by jpipe runner")

        for cls in self._model.class_defs:
            match cls.class_type:
                case ClassType.JUSTIFICATION:
                    # expand justification with pattern.
                    if cls.pattern is not None:
                        jd: JustificationDef = self._find_pattern(cls.pattern)
                        cls.body.supports.update(i for i in jd.supports)
                        cls.body.variables.update(i for i in jd.variables
                                                  if i.var_type != VariableType.SUPPORT)
                    self._validate_justification(cls.body)
                case ClassType.PATTERN:
                    # ignore pattern class
                    pass
                case ClassType.COMPOSITION:
                    # ignore composition class
                    pass

    def _find_pattern(self, pattern: str) -> JustificationDef:
        for cls in self._model.class_defs:
            if cls.class_type == ClassType.PATTERN and cls.name == pattern:
                assert isinstance(cls.body, JustificationDef)
                return cls.body
        raise InvalidJustificationException(f"pattern {pattern} not found")

    def _validate_justification(self, jd: JustificationDef) -> None:
        return

    def load_jd(self, jd_file: str) -> None:
        parse_jd_file(filename=jd_file)
        pass
