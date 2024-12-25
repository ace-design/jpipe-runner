"""
jpipe_runner.utils
~~~~~~~~~~~~~~~~~~

This module contains the utilities of jPipe Runner.
"""

import json
import re


def unquote_string(s: str) -> str:
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f'{repr(s)} is not a valid STRING') from e


def sanitize_string(s: str) -> str:
    # Use re to keep only allowed characters.
    sanitized = re.sub(r'[^a-z0-9_]', '',
                       re.sub(r'\s+', '_', s.lower()))
    return sanitized


def _test():
    """test unquote_string"""
    assert unquote_string('"hello"') == 'hello'
    try:
        unquote_string("'hello'")
    except ValueError:
        pass

    """test sanitize_string"""
    assert sanitize_string('Hello, world!') == 'hello_world'
    assert sanitize_string('Check  contents w.r.t. NDA') == 'check_contents_wrt_nda'
    assert sanitize_string('Check PEP8 coding standard') == 'check_pep8_coding_standard'


if __name__ == "__main__":
    _test()
