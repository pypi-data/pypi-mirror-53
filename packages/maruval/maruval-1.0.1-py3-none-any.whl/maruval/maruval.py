from __future__ import print_function

import argparse
import json
import os
import sys

from jsonschema import Draft7Validator
from jsonschema import validate as schema_validate
from jsonschema.exceptions import ValidationError

# elements that contain either a filepath or a list of them
IS_FILEPATH = {
    "from",
    "to",
    "images",
    "image",
    "video",
    "icon",
    "speech",
    "pageTransition",
    "mail",
    "page",
    "affectedPage",
    "affectedDialogResponse",
    "affectedMail",
    "affectedExercise",
    "startPage",
    "audio",
}


def _parse_cmdline_args():
    """
    Command line argument parsing. Doing it here means less duplication than
    would be the case in bin/

    Returns command line arguments as a dict
    """
    parser = argparse.ArgumentParser(description="Validate marugoto game content.")

    parser.add_argument(
        "-nw",
        "--no-warnings",
        default=True,
        action="store_true",
        required=False,
        help="Do not show warnings",
    )

    parser.add_argument(
        "-f",
        "--fail-first",
        default=False,
        action="store_true",
        required=False,
        help="Stop after first error",
    )

    parser.add_argument("path", help="Path to the files")

    return vars(parser.parse_args())


def _get_json_files(path):
    """
    Recursively get JSON files.
    """
    path = os.path.abspath(os.path.expanduser(path))
    print("\nValidating content at {}".format(path))
    out = [path] if os.path.isfile(path) else list()
    if not out:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".json"):
                    out.append(os.path.join(root, file))
    if not out:
        raise OSError("No .json found at {}.".format(os.path.abspath(path)))
    elif not os.path.isfile(path):
        print("{} JSON files found.".format(len(out)))
    return out


def _get_schemata():
    """
    Load all our JSON schemata into a dict with file basenames as keys
    """
    schemata = dict()
    # hopfully, find the schemata folder?
    data_dir = _locate_schemata_dir()
    jsons = [i for i in os.listdir(data_dir) if i.endswith(".json")]
    for jso in jsons:
        with open(os.path.join(data_dir, jso), "r") as fo:
            loaded = json.load(fo)
        schemata[os.path.splitext(jso)[0]] = loaded
    return schemata


def _print_errors(errors):
    """
    Nicely print out errors
    """
    eq = "=" * 100
    mi = "-" * 100
    print("\n" + eq)
    for i, (err, filename, invalid_syntax) in enumerate(errors, start=1):
        # add line number of syntax errors
        if invalid_syntax:
            filename = "{}:{}".format(filename, err.lineno)
        errname = "Content" if not invalid_syntax else "Syntax"
        form = "Problem #{} -- {} error in {}\n{}\n\n{}\n\n{}"
        print(form.format(i, errname, filename, mi, err, eq))


def _get_correct_schema(json_file, schemata):
    """
    Get correct validation schema based on filename
    """
    no_ext = os.path.basename(os.path.splitext(json_file)[0])
    schema_name = "".join([i for i in no_ext if i.isalpha()])
    Draft7Validator.check_schema(schemata[schema_name])
    return schema_name, schemata[schema_name]


def _locate_schemata_dir():
    """
    schemata dir seems to move around depending on how you install!?
    """
    fpath = os.path.dirname(__file__)
    first = os.path.dirname(fpath)
    second = os.path.dirname(first)
    third = sys.prefix
    fourth = os.path.join(third, "maruval")
    fifth = os.path.expanduser("~/marugoto-validator")
    dirs = [first, second, third, fourth, fifth]
    for path in dirs:
        full = os.path.join(path, "schemata")
        if os.path.isdir(full):
            return full
    raise ValueError("No schemata dir found at: {}".format(dirs))


def _custom_validate(fname, data):
    """
    Custom validation for files. Right now, just check filepath is valid.
    """
    for key, value in data.items():
        if isinstance(value, dict):
            _custom_validate(fname, value)
        if key not in IS_FILEPATH:
            continue
        to_check = value if isinstance(value, list) else [value]
        for item in to_check:
            if item is None:
                continue
            error = "{} has key '{}', but {} not found.".format(fname, key, item)
            if not os.path.isfile(item):
                raise OSError(error)


def validate(path=None, fail_first=False, no_warnings=False):
    """
    Main validator routine

    Iterate over all JSON files, check that they can be loaded, and then run jsonschema.
    Handle fail fast option both during loading and validating.
    """
    errors = list()
    to_check = _get_json_files(path)
    schemata = _get_schemata()
    ok = 0
    for json_file in sorted(to_check):
        schema_name, schema = _get_correct_schema(json_file, schemata)
        with open(json_file, "r") as f:
            try:
                data = json.load(f)
            except Exception as err:
                errors.append((err, json_file, True))
                if fail_first:
                    break
                continue
        try:
            schema_validate(instance=data, schema=schema)
            _custom_validate(json_file, data)

        except (ValidationError, OSError) as err:
            errors.append((err, json_file, False))
            if fail_first:
                break
            continue
        ok += 1
    _print_errors(errors)
    msg = "\nAll done. {} errors found".format(len(errors))
    if len(to_check) > 1:
        msg += ". {} files OK.\n".format(ok)
    else:
        msg += " in {}".format(to_check[0])
    print(msg)


if __name__ == "__main__":
    validate(**_parse_cmdline_args())
