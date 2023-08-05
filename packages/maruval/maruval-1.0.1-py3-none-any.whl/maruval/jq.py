import os
import stat
import sys

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

WINLINK = "https://stedolan.github.io/jq/"
RELEASE = "https://github.com/stedolan/jq/releases/download/jq-1.6"

LINKS = dict(
    linux=("{}/jq-linux64".format(RELEASE), "/usr/bin/jq"),
    darwin=("{}/jq-osx-amd64".format(RELEASE), "/usr/local/bin/jq"),
)


def configure():
    """
    Installs jq.

    Usage: sudo python -m maruval.jq
    """
    print("Configuring jq...")
    try:
        url, dest = LINKS[sys.platform]
    except KeyError:
        msg = "Cannot autoinstall jq for {}. Do it yourself via {}".format(
            sys.platform, WINLINK
        )
        raise OSError(msg)
    urlretrieve(url, dest)
    # make executable
    os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)
    print("Installed jq to {}".format(dest))


if __name__ == "__main__":
    configure()
