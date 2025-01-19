"""
jpipe_runner.parser
~~~~~~~~~~~~~~~~~~~

This module contains the parser code of jPipe Runner.
"""

import json
import os

from lark import Lark, ParseTree
from lark.exceptions import (UnexpectedCharacters,
                             UnexpectedToken)

from jpipe_runner.transformer import *


def read_jpipe_grammar() -> str:
    lark_file = os.path.join(
        os.path.dirname(__file__),
        'jpipe.lark')
    with open(lark_file, encoding='utf-8') as f:
        return f.read()


JPIPE_GRAMMAR = read_jpipe_grammar()

# Default jPipe parser.
jpipe_parser = Lark(grammar=JPIPE_GRAMMAR,
                    start='start',
                    parser='lalr')


def parse_jd(source: str) -> ModelDef:
    try:
        tree: ParseTree = jpipe_parser.parse(text=source)
        model: ModelDef = JPipeTransformer().transform(tree)
        return model
    except (UnexpectedCharacters, UnexpectedToken) as e:
        raise SyntaxException(
            'parse error: invalid justification diagram source code') from e


def parse_jd_file(filename: str) -> ModelDef:
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    return parse_jd(source=content)


def parse_jd_json(json_data: dict) -> ModelDef:
    def parse_supports(supports):
        return {SupportDef(**support) for support in supports}

    def parse_variables(variables):
        return {
            key: VariableDef(
                var_type=VariableType(variable["var_type"]),
                name=variable["name"],
                description=variable["description"]
            )
            for key, variable in variables.items()
        }

    def parse_justification(body):
        return JustificationDef(
            supports=parse_supports(body["supports"]),
            variables=parse_variables(body["variables"])
        )

    def parse_class_defs(class_defs):
        return {
            key: ClassDef(
                class_type=ClassType(value["class_type"]),
                name=value["name"],
                pattern=value["pattern"],
                body=parse_justification(value["body"])
            )
            for key, value in class_defs.items()
        }

    return ModelDef(
        load_stmts=set(json_data["load_stmts"]),
        class_defs=parse_class_defs(json_data["class_defs"])
    )


def parse_jd_json_file(filename: str) -> ModelDef:
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)
    return parse_jd_json(json_data=data)


def load_jd_file(filename: str, _loaded: set = None) -> ModelDef:
    """load_jd_file is able to load JD files recursively."""

    if _loaded is None:
        _loaded = set()
    if (jd_file := os.path.abspath(filename)) in _loaded:
        raise RecursionError(f"justification file '{filename}' already loaded")

    # save loaded JD file path
    _loaded.add(jd_file)

    model = parse_jd_file(filename=jd_file)

    for ld in model.load_stmts.copy():
        new_model = load_jd_file(ld.path, _loaded)
        model.update(new_model)

    return model


def _test():
    pass


if __name__ == "__main__":
    _test()
