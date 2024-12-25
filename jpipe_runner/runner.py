"""
jpipe_runner.runner
~~~~~~~~~~~~~~~~~~~

This module contains the entrypoint of jPipe Runner.
"""

import argparse
import fnmatch
import shutil
import sys
from typing import Iterable

from termcolor import colored

from jpipe_runner.enums import StatusType
from jpipe_runner.jpipe import JPipeEngine
from jpipe_runner.runtime import PythonRuntime

# Generate:
# - https://patorjk.com/software/taag/#p=display&f=Ivrit&t=jPipe%20%20Runner%0A
JPIPE_RUNNER_ASCII = r"""
    _ ____  _               ____                              
   (_)  _ \(_)_ __   ___   |  _ \ _   _ _ __  _ __   ___ _ __ 
   | | |_) | | '_ \ / _ \  | |_) | | | | '_ \| '_ \ / _ \ '__|
   | |  __/| | |_) |  __/  |  _ <| |_| | | | | | | |  __/ |   
  _/ |_|   |_| .__/ \___|  |_| \_\\__,_|_| |_|_| |_|\___|_|   
 |__/        |_|                                                                                     
"""


def parse_args(argv=None):
    parser = argparse.ArgumentParser(prog="jpipe_runner",
                                     description=("McMaster University - McSCert (c) 2023-..."
                                                  + JPIPE_RUNNER_ASCII),
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--variable", "-v", action="append", default=[],
                        help="Define a variable in the format NAME:VALUE")
    parser.add_argument("--library", "-l", action="append", default=[],
                        help="Specify a Python library to load")
    parser.add_argument("--diagram", "-d", metavar="PATTERN", default="*",
                        help="Specify diagram pattern or wildcard")
    # parser.add_argument("--output", "-o", metavar="FILE",
    #                     help="Output file for generated diagram image")
    parser.add_argument("--dry-run", action="store_true",
                        help="Perform a dry run without actually executing justifications")
    # parser.add_argument("--verbose", "-V", action="store_true",
    #                     help="Enable verbose (debug) output")
    parser.add_argument("jd_file",
                        help="Path to the justification .jd file")

    return parser.parse_args(argv)


def pretty_display(diagrams: Iterable[tuple[str, Iterable[dict]]]) -> [int, int, int, int]:
    terminal_width, _ = shutil.get_terminal_size((78, 30))
    width = 78 if terminal_width > 78 else terminal_width

    colored_statuses = {
        StatusType.PASS: colored(StatusType.PASS.value, color="green"),
        StatusType.FAIL: colored(StatusType.FAIL.value, color="red"),
        StatusType.SKIP: colored(StatusType.SKIP.value, color="yellow"),
    }

    jpipe_title = colored("jPipe Files", color=None, attrs=[])

    total_justifications = 0
    passed_justifications = 0
    failed_justifications = 0
    skipped_justifications = 0

    print("=" * width)
    print(f"{jpipe_title}".ljust(width))
    print("=" * width)

    for name, result in diagrams:

        total_justifications += 1

        print(f"{jpipe_title}.Justification :: {name}".ljust(width))
        print("=" * width)

        is_passed = True
        is_failed = False
        is_skipped = []

        for data in result:

            var_type = data['var_type'].value.title()
            var_name = data['name']
            label = data['label']
            exception = data.get('exception')
            status = data['status']
            len_status = len(f"| {status.value} |")
            status_bar = f"| {colored_statuses[status]} |"

            if status != StatusType.PASS:
                is_passed = False

            if status == StatusType.FAIL:
                is_failed = True

            is_skipped.append(True if status == StatusType.SKIP else False)

            if exception:
                print(exception.ljust(width))

            print(f"{var_type}<{var_name}> :: {label}".ljust(width - len_status) + status_bar)
            print("-" * width)

        if is_passed:
            passed_justifications += 1

        if is_failed:
            failed_justifications += 1

        if all(is_skipped):
            skipped_justifications += 1

    print(f"{jpipe_title}")
    print(f"{total_justifications} justifications,",
          f"{passed_justifications} passed,",
          f"{failed_justifications} failed,",
          f"{skipped_justifications} skipped",
          )
    print("=" * width)

    return total_justifications, passed_justifications, failed_justifications, skipped_justifications


def main():
    args = parse_args(sys.argv[1:])

    jpipe = JPipeEngine(jd_file=args.jd_file)

    diagrams = [jd for jd in jpipe.justifications.keys()
                if fnmatch.fnmatch(jd, args.diagram)]

    if not diagrams:
        print(f"No justification diagram found: {args.diagram}")
        sys.exit(1)

    runtime = PythonRuntime(libraries=args.library,
                            variables=[i.split(':', maxsplit=1)
                                       for i in args.variable])

    m, n, _, _ = pretty_display((d, jpipe.justify(d,
                                                  dry_run=args.dry_run,
                                                  runtime=runtime.copy()))
                                for d in diagrams)
    # exit 0 when all justifications passed
    sys.exit(m - n)


if __name__ == '__main__':
    main()
