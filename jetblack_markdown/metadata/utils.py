"""Meta data utilities"""

import inspect
import sys
from types import ModuleType
from typing import Any, Optional, Type


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


def is_named_tuple_type(obj: Type) -> bool:
    """Check if a type is a named tuple

    Args:
        obj (Type): The type to check

    Returns:
        bool: True if the type is a named tuple.
    """
    if tuple not in getattr(obj, '__bases__', []):
        return False

    fields = getattr(obj, '_fields', None)
    if not isinstance(fields, tuple):
        return False

    return all(isinstance(field, str) for field in fields)


def is_child_module(parent: ModuleType, child: Any) -> bool:
    """Check if a module is a child of another module

    Args:
        parent ([type]): The parent module
        child ([type]): The child to test

    Returns:
        bool: True if the child is a child module of the parent
    """

    return (
        inspect.ismodule(child) and
        getattr(child, '__package__', '').startswith(
            getattr(parent, '__package__', '')
        )
    )
