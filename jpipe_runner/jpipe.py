"""
jpipe_runner.jpipe
~~~~~~~~~~~~~~~~~~

This module contains the core of jPipe Runner.
"""

from copy import deepcopy

from jpipe_runner.enums import ClassType, VariableType
from jpipe_runner.exceptions import UnsupportedException, NotFoundException
from jpipe_runner.models import ModelDef, JustificationDef


class JPipe:

    def __init__(self,
                 model: ModelDef,
                 ):
        self.model = deepcopy(model)
        self.init_model()

    def init_model(self) -> None:
        if len(self.model.load_stmts) > 0:
            raise UnsupportedException("load statement is not supported by jpipe runner")

        for cls in self.model.class_defs:
            match cls.class_type:
                case ClassType.JUSTIFICATION:
                    # expand pattern to justification.
                    if cls.pattern is not None:
                        jd: JustificationDef = self.find_pattern(cls.pattern)
                        cls.body.supports.update(i for i in jd.supports)
                        cls.body.variables.update(i for i in jd.variables
                                                  if i.var_type != VariableType.SUPPORT)
                case ClassType.PATTERN:
                    # ignore pattern class
                    pass
                case ClassType.COMPOSITION:
                    # ignore composition class
                    pass

    def find_pattern(self, pattern: str) -> JustificationDef:
        for cls in self.model.class_defs:
            if cls.class_type == ClassType.PATTERN and cls.name == pattern:
                assert isinstance(cls.body, JustificationDef)
                return cls.body
        raise NotFoundException(f"pattern {pattern} not found")
