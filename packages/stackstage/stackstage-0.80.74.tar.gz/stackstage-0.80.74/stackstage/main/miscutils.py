
import os
import stat
import yaml
from datetime import datetime


def serialize(item):
    """Return string version of item"""
    if isinstance(item, datetime):
        return item.isoformat() + "Z"
    return str(item)


def random_string(size=12):
    """Return randomn string of length size"""
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for i in range(size)])


def verify_http(response):
    """Filter out statuscode from a response"""
    try:
        statuscode = response['ResponseMetadata']['HTTPStatusCode']
        if not isinstance(statuscode, int):
            raise KeyError
    except KeyError:
        return None, 500

    return response, statuscode


def readyaml(filename):
    """Read a yaml file and return its contents"""
    with open(filename, 'r') as yamlfile:
        return yaml.safe_load(yamlfile)


def list_regfiles(directory, root='', recursive=False, files={}):
    """Returns a dictonary of regular files in a directory.
    Key is pathname within root, Value is pathname on system."""
    if not isinstance(directory, str):
        raise TypeError("directory should be formatted as string")
    if not os.path.isdir(directory) is True:
        raise ValueError("directory does not exist: " + directory)

    for filename in os.listdir(directory):
        pathname = os.path.join(directory, filename)
        mode = os.stat(pathname).st_mode
        if stat.S_ISDIR(mode) and recursive is True:
            list_regfiles(pathname,
                          root=os.path.join(root, filename),
                          recursive=True,
                          files=files)
        elif stat.S_ISREG(mode):
            files[os.path.join(root, filename)] = pathname

    return files
