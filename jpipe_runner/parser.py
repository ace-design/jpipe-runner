"""
jpipe_runner.parser
~~~~~~~~~~~~~~~~~~~

This module contains the parser code of jPipe Runner.
"""

import os

from lark import Lark, ParseTree
from lark.exceptions import (UnexpectedCharacters,
                             UnexpectedToken)

from jpipe_runner.jpipe import JPipe
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


def parse_justification_diagram(source: str) -> ParseTree:
    try:
        tree = jpipe_parser.parse(text=source)
        return tree
    except (UnexpectedCharacters, UnexpectedToken) as e:
        raise SyntaxException(
            'parse error: invalid justification diagram source code') from e


def test():
    for ff in (
            # 'examples/01_slides.jd',
            # "examples/02_quality_full.jd",
            # "examples/03_quality_compo.jd",
            "examples/04_pattern.jd",
    ):
        with open(
                ff
        ) as f:
            text = f.read()
            tree = parse_justification_diagram(text)

        model = JPipeTransformer().transform(tree)
        jpipe = JPipe(model)

        from pprint import pprint
        pprint(jpipe.model)


if __name__ == "__main__":
    test()
