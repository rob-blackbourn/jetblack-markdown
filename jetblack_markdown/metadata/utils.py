"""Meta data utilities"""

import sys
from typing import Optional


def make_file_relative(file: Optional[str]) -> Optional[str]:
    """Make a file path relative

    Args:
        file (Optional[str]): The file path

    Returns:
        Optional[str]: The relative file path
    """
    if file is None:
        return None

    for path in sys.path:
        if file.startswith(path):
            return file[len(path)+1:]

    return file
