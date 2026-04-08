__author__ = "Lukas Mahler"
__version__ = "0.3.1"
__date__ = "08.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


import os
import re
import sys
from typing import Literal

IGNORED_FILES = {"econ_pb2.py"}

def get_pyproject_version() -> str | None:
    """
    Read the version from pyproject.toml in the repository root.

    :return: The version string from pyproject.toml, or None if not found.
    :rtype: str | None
    """

    pyproject_path = os.path.join(os.path.dirname(__file__), '..', 'pyproject.toml')
    pyproject_path = os.path.normpath(pyproject_path)

    if not os.path.isfile(pyproject_path):
        return None

    with open(pyproject_path, 'r', encoding='UTF-8') as f:
        content = f.read()

    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    return match.group(1) if match else None


def check_version_match(file_path: str, expected_version: str) -> bool:
    """
    Check if the '__version__' variable in a Python file matches the expected version, and update it if necessary.

    :param file_path: The path to the Python file to check and potentially update.
    :type file_path: str
    :param expected_version: The expected version string from pyproject.toml.
    :type expected_version: str

    :return: True if the '__version__' variable was already correct or was updated.
    :rtype: bool
    """

    with open(file_path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    update_file = False
    for i, line in enumerate(lines):
        if line.strip().startswith('__version__'):
            version_from_file = line.strip().split('=')[1].strip().strip('"\'')
            if version_from_file != expected_version:
                update_file = True
                lines[i] = f'__version__ = "{expected_version}"\n'
            break

    if update_file:
        with open(file_path, 'w', encoding='UTF-8') as file:
            file.writelines(lines)

    return True


def check_hook(files: list[str]) -> Literal[0, 1]:
    """
    Check and update the '__version__' variable in modified Python files to match pyproject.toml.

    :param files: A list of file paths to check for modification.
    :type files: list[str]

    :return: 0 if all '__version__' variables were correct or updated, 1 otherwise.
    :rtype: Literal[0, 1]
    """

    expected_version = get_pyproject_version()
    if expected_version is None:
        print("Could not read version from pyproject.toml")
        return 1

    py_files = [
        file_path
        for file_path in files
        if file_path.endswith('.py')
        and os.path.isfile(file_path)
        and os.path.basename(file_path) not in IGNORED_FILES
    ]
    for file_path in py_files:
        if not check_version_match(file_path, expected_version):
            return 1
    return 0


if __name__ == '__main__':
    changed_files = sys.argv[1:]
    sys.exit(check_hook(changed_files))
