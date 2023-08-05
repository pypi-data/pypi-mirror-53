from __future__ import print_function

import argparse
import os
import re


def _parse_cmdline_args():
    """
    Command line argument parsing. Doing it here means less duplication than
    would be the case in bin/

    Returns command line arguments as a dict
    """
    desc = "Find directories containing all of the specified file types"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        "-not",
        "--inverse",
        default=False,
        action="store_true",
        required=False,
        help="Invert the matching criteria",
    )

    parser.add_argument(
        "-r",
        "--regex",
        default=False,
        action="store_true",
        required=False,
        help="Use regular expression search",
    )

    parser.add_argument(
        "-t",
        "--times",
        default=1,
        type=int,
        required=False,
        help="Minimum number of occurrences",
    )

    parser.add_argument(
        "-p",
        "--pattern",
        type=str,
        required=True,
        help="Pattern to be searched",
    )

    parser.add_argument("path", help="Path to the data directory")

    return vars(parser.parse_args())


def _explain(inverse, pattern, times, path):
    """
    Print a plain-language explanation of the search
    """
    do_not = "NOT " if inverse else ""
    path = os.path.abspath(path)
    form = 'Find files in {} {}containing {} instances of "{}"'
    print(form.format(path, do_not, times, pattern))


def _check_file(path, pattern, times, inverse, regex):
    """
    Does file at this path contain pattern at least n times?
    """
    with open(path, 'r') as fo:
        text = fo.read()
    count = text.count(pattern) if not regex else len(re.findall(pattern, text))
    match = count >= int(times)
    return match if not inverse else not match


def searcher(inverse=False, pattern=None, times=1, path=None, regex=False):
    eq = "=" * 80
    mi = "-" * 80
    print(eq)
    path = os.path.expanduser(path)
    _explain(inverse, pattern, times, path)
    print(mi)
    for root, _, files in os.walk(path):
        for fname in sorted(files):
            if not fname.endswith('.json'):
                continue
            path = os.path.join(root, fname)
            if _check_file(path, pattern, times, inverse, regex):
                print("Matching file: {}".format(path))
    print(eq)


if __name__ == "__main__":
    searcher(**_parse_cmdline_args())
