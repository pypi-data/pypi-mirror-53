import os
import shutil
import subprocess

from .maruval import _locate_schemata_dir


def configure():
    """
    python -m maruval.atom
    """
    print("Configuring maruval for Atom...")
    target = os.path.join(_locate_schemata_dir(), "process-palette.json")
    assert os.path.isfile(target), "Does not exist: {}".format(target)
    shutil.copyfile(target, os.path.expanduser("~/.atom/process-palette.json"))
    subprocess.call("apm install process-palette".split())
    subprocess.call("apm install tree-view-auto-reveal".split())
    msg = "maruval for atom configured. "
    msg += "restart atom and type 'maruval' in command palette..."
    print(msg)


if __name__ == "__main__":
    configure()
