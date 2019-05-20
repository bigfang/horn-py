import tempfile
import shutil
import subprocess

from pathlib import Path


TPL_PATH = Path(__file__).parent.joinpath('templates')


def convert_path(path):
    rv = path
    if not (path.startswith('http') or path.startswith('git@') or path.startswith('ssh://')):
        rv = str(Path(path).resolve())
    return rv


def get_location(bindings):
    location = bindings.get('from')
    if location and (location.startswith('http') or location.startswith('git@') or location.startswith('ssh://')):
        location = clone(bindings.get('from'), bindings.get('checkout'))
    return location


def clone(url, checkout=None):
    location = tempfile.mkdtemp()
    shutil.rmtree(location)  # Path must not exists
    subprocess.check_call(["git", "clone", url, location])
    if checkout:
        subprocess.check_call(["git", "checkout", checkout], cwd=location)
    return location
