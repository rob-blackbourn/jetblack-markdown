"""Mocks"""

from typing import Any, List, Optional

DEFAULT_INT = 1


def mock_func(arg_one: str, arg_two: Optional[int] = DEFAULT_INT) -> List[Any]:
    """The short description

    The long description

    Args:
        arg_one (str): The first argument
        arg_two (Optional[int], optional): The second argument. Defaults to DEFAULT_INT.

    Raises:
        RuntimeException: The raises description

    Returns:
        List[Any]: The return description
    """
    return [arg_one, arg_two]
