"""
jpipe_runner.utils
~~~~~~~~~~~~~~~~~~

This module contains the utilities of jPipe Runner.
"""

import json


def unquote_string(s: str) -> str:
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f'{repr(s)} is not a valid STRING') from e


def _test_unquote_string():
    assert unquote_string('"hello"') == 'hello'
    try:
        unquote_string("'hello'")
    except ValueError:
        pass


def _test():
    _test_unquote_string()


if __name__ == "__main__":
    _test()
