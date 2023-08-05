from __future__ import print_function

import argparse
import os

JSON_TYPES = {
    "audiocomponent",
    "chapter",
    "character",
    "checkboxexercise",
    "dateexercise",
    "dialog",
    "dialogresponse",
    "dialogspeech",
    "imagecomponent",
    "linkcomponent",
    "mail",
    "notebookentry",
    "page",
    "pagetransition",
    "radiobuttonexercise",
    "textcomponent",
    "textexercise",
    "topic",
    "uploadexercise",
    "videocomponent",
}


def listed(s):
    got = [i.strip().lower() for i in s.split(",")]
    if not got:
        raise ValueError(
            "Please provide one or more JSON file types, separated by comma"
        )
    return got


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
        "-any",
        "--any-of",
        default=False,
        action="store_true",
        required=False,
        help="Get any, not all directories containing these files",
    )

    parser.add_argument(
        "-only",
        "--only",
        default=False,
        action="store_true",
        required=False,
        help="Get directories containing only these files (any/all will be ignored)",
    )

    parser.add_argument(
        "-atom",
        "--atom",
        default=False,
        action="store_true",
        required=False,
        help="Atom compatibility mode",
    )

    parser.add_argument(
        "json_types", type=listed, help="Comma-separated list of JSON file types"
    )

    parser.add_argument("path", help="Path to the data directory")

    return vars(parser.parse_args())


def _explain(inverse, any_of, only, json_types, path):
    """
    Print a plain-language explanation of the search
    """
    any_all = "any of" if any_of else "all of"
    if only:
        any_all = "only"
    do_not = "NOT " if inverse else ""
    types = "\n\t*".join(sorted(json_types))
    exp = "Finding dirs in {} where {} the following files are {}present:\n\t*{}\n"
    print(exp.format(path, any_all, do_not, types))


def _check_folder(folder, inverse, any_of, only, json_types):
    files = [i for i in os.listdir(folder) if i.endswith(".json")]
    files = [os.path.splitext(i)[0].lower() for i in files]
    files = ["".join(x for x in i if x.isalpha()) for i in files]
    if only:
        match = all(i in json_types for i in files)
    else:
        matcher = any if any_of else all
        match = matcher(f in files for f in json_types)
    return match if not inverse else not match


def _get_first_file(folder, atom):
    """
    Get a representative file from this folder for quicklinking in atom
    """
    if not atom:
        return ""
    files = [
        i
        for i in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, i)) and not i.startswith(".")
    ]
    if files:
        return sorted(files)[0]
    return ""


def finder(
    inverse=False, any_of=False, only=False, json_types=None, path=None, atom=False
):
    eq = "=" * 80
    mi = "-" * 80
    print(eq)
    path = os.path.expanduser(path)
    _explain(inverse, any_of, only, json_types, path)
    print(mi)
    for root, dirs, _ in os.walk(path):
        for folder in sorted(dirs):
            folder = os.path.join(root, folder)
            if _check_folder(folder, inverse, any_of, only, json_types):
                first_file = _get_first_file(folder, atom)
                form = os.path.join(os.path.abspath(folder), first_file).rstrip("/")
                print("Matching directory: {}".format(form))
    print(eq)


if __name__ == "__main__":
    finder(**_parse_cmdline_args())
