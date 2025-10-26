__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "26.10.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


import datetime
import os
import sys
from typing import Literal

IGNORED_FILES = {"econ_pb2.py"}


def check_date_match(file_path: str) -> bool:
    """
    Check if the '__date__' variable in a Python file matches the current date, and update it if necessary.

    :param file_path: The path to the Python file to check and potentially update.
    :type file_path: str

    :return: True if the '__date__' variable is found and matches the current date or is updated, False otherwise.
    :rtype: bool
    """

    date_format = "%d.%m.%Y"
    current_date = datetime.datetime.now().strftime(date_format)
    file_modification_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(date_format)
    if file_modification_date != current_date:
        # Ignore files that haven't been modified today
        return True

    with open(file_path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    update_file = date_exists = False
    for i, line in enumerate(lines):
        if line.strip().startswith('__date__'):
            date_exists = True
            date_from_file = line.strip().split('=')[1].strip().strip('"\'')
            if date_from_file != current_date:
                update_file = True
                lines[i] = f'__date__ = "{current_date}"\n'
            break

    if not date_exists:
        print(f"Variable '__date__' not found in file: {file_path}")
        lines.insert(0, f'__date__ = "{current_date}"\n')
        update_file = True

    if update_file:
        with open(file_path, 'w', encoding='UTF-8') as file:
            file.writelines(lines)

    return True


def check_hook(files: list[str]) -> Literal[0, 1]:
    """
    Check and update the '__date__' variable in modified Python files.

    :param files: A list of file paths to check for modification.
    :type files: list[str]

    :return: 0 if all '__date__' variables in modified files match the current date or are updated, 1 otherwise.
    :rtype: Literal[0, 1]
    """

    # Get list of modified .py files
    py_files = [
        file_path
        for file_path in files
        if file_path.endswith('.py')
        and os.path.isfile(file_path)
        and os.path.basename(file_path) not in IGNORED_FILES
    ]
    for file_path in py_files:
        if not check_date_match(file_path):
            return 1
    return 0


if __name__ == '__main__':
    changed_files = sys.argv[1:]
    sys.exit(check_hook(changed_files))
