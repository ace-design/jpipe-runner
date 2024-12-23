"""
jpipe_runner.jpipe
~~~~~~~~~~~~~~~~~~

This module contains the core of jPipe Runner.
"""

from typing import Optional

from jpipe_runner.enums import ClassType
from jpipe_runner.exceptions import InvalidJustificationException
from jpipe_runner.models import ModelDef, JustificationDef
from jpipe_runner.parser import load_jd_file


class Justification:
    pass


class JPipe:

    def __init__(self,
                 jd_file: Optional[str] = None,
                 ):
        self._model: ModelDef = ModelDef()

        if jd_file:
            self.load_jd_file(filename=jd_file)

        self._init_model()

    # load justification file to class model
    def load_jd_file(self, filename: str) -> None:
        model = load_jd_file(filename)
        self._model.update(model)

    def _init_model(self) -> None:
        for cls in self._model.class_defs.values():
            match cls.class_type:
                case ClassType.JUSTIFICATION:
                    # expand justification with pattern.
                    # if cls.pattern is not None:
                    #     jd: JustificationDef = self._find_pattern(cls.pattern)
                    #     cls.body.supports.update(i for i in jd.supports)
                    #     cls.body.variables.update(i for i in jd.variables
                    #                               if i.var_type != VariableType.SUPPORT)
                    # self._validate_justification(cls.body)
                    pass
                case ClassType.PATTERN:
                    # ignore pattern class.
                    pass
                case ClassType.COMPOSITION:
                    # ignore composition class.
                    pass

    def _find_pattern(self, pattern: str) -> JustificationDef:
        for cls in self._model.class_defs.values():
            if cls.class_type == ClassType.PATTERN and cls.name == pattern:
                assert isinstance(cls.body, JustificationDef)
                return cls.body
        raise InvalidJustificationException(f"pattern {pattern} not found")

    def _validate_justification(self, jd: JustificationDef) -> None:
        return
