"""
jpipe_runner.runner
~~~~~~~~~~~~~~~~~~~

This module contains the entrypoint of jPipe Runner.
"""

import argparse
import fnmatch
import sys

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

    for d in diagrams:
        jpipe.justify(d,
                      dry_run=args.dry_run,
                      runtime=runtime.copy())


if __name__ == '__main__':
    main()
