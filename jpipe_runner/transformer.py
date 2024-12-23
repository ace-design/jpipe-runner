"""
jpipe_runner.transformer
~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the transformer for jPipe Lark Grammar.
"""

from typing import Any, Iterable

import lark
from lark import Transformer, v_args

from jpipe_runner import utils
from jpipe_runner.enums import (ClassType,
                                VariableType)
from jpipe_runner.exceptions import SyntaxException
from jpipe_runner.models import (ModelDef,
                                 LoadStmt,
                                 ClassDef,
                                 VariableDef,
                                 SupportDef,
                                 JustificationDef,
                                 CompositionDef)


# noinspection PyMethodMayBeStatic
class JPipeTransformer(Transformer):
    @v_args(inline=True)
    def start(self, model: ModelDef) -> ModelDef:
        return model

    def model(self, items: Iterable[LoadStmt | ClassDef]) -> ModelDef:
        return ModelDef(
            load_stmts=[item for item in items if isinstance(item, LoadStmt)],
            class_defs=[item for item in items if isinstance(item, ClassDef)],
        )

    @v_args(inline=True)
    def load_stmt(self, path: str) -> LoadStmt:
        return LoadStmt(path=path)

    @v_args(inline=True)
    def class_def(self,
                  class_type: ClassType,
                  name: str,
                  *params) -> ClassDef:
        cls = ClassDef(class_type=class_type,
                       name=name)
        if num := len(params) not in (1, 2):
            raise SyntaxError(f"invalid number of parameters: {num}")

        if isinstance(body := params[-1], JustificationDef | CompositionDef):
            cls.body = body
        else:
            raise SyntaxError(f"invalid class body: {type(body)}")

        match len(params):
            case 2:
                if class_type != ClassType.JUSTIFICATION:
                    raise SyntaxException(
                        f"Keyword implements is only supported for {ClassType.JUSTIFICATION}, but is used in {class_type}")
                cls.pattern = params[0]

        return cls

    def justification_pattern(self,
                              items: Iterable[VariableDef | SupportDef],
                              ) -> JustificationDef:
        return JustificationDef(
            variables=set(i for i in items if isinstance(i, VariableDef)),
            supports=set(i for i in items if isinstance(i, SupportDef)),
        )

    @v_args(inline=True)
    def variable(self,
                 var_type: VariableType,
                 name: str,
                 description: str,
                 ) -> VariableDef:
        return VariableDef(var_type=var_type,
                           name=name,
                           description=description)

    @v_args(inline=True)
    def instruction(self, desc: str) -> str:
        return desc

    @v_args(inline=True)
    def support(self,
                left: str,
                right: str,
                ) -> SupportDef:
        return SupportDef(left=left,
                          right=right)

    def composition(self, items: Iterable[Any]) -> CompositionDef:
        return CompositionDef(
            compositions=set(i for i in items),
        )

    # TODO: add support for composition class.
    # def composition_variable(self, items):
    #     return {"composition_variable": {"justification": items[0]}}
    #
    # def composition_instruction(self, items):
    #     return {"composition_instruction": {"variable": items[0], "information": items[1]}}
    #
    # def composition_information(self, items):
    #     return {"information": {"id1": items[0], "id2": items[1]}}

    # LEXER tokens
    def CLASS_TYPE(self, token: lark.Token) -> ClassType:
        return ClassType(token.value)

    def VARIABLE_TYPE(self, token: lark.Token) -> VariableType:
        return VariableType(token.value)

    def ID(self, token: lark.Token) -> str:
        return str(token.value)

    def STRING(self, token: lark.Token) -> str:
        return utils.unquote_string(token.value)
