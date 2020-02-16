"""Mocks"""

from typing import Any, List, NamedTuple, Optional, Tuple

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


def mock_func_with_kwargs(
        arg_one: int,
        *,
        arg_two: str,
        arg_three: Optional[float] = None
) -> Tuple[int, str, Optional[float]]:
    """A function with keyword arguments

    Args:
        arg_one (int): The first positional argument
        arg_two (str): The first keyword argument
        arg_three (Optional[float], optional): The second keyword argument. Defaults to None.

    Returns:
        Tuple[int, str, Optional[float]]: The args returned
    """
    return arg_one, arg_two, arg_three


class MockClass:
    """A mock class"""

    def __init__(self, arg1: str) -> None:
        """Initialise the class

        Args:
            arg1 (str): The first arg
        """
        self.arg1 = arg1

    @classmethod
    def a_class_method(cls, arg1: str) -> Optional[str]:
        """A class method

        Args:
            arg1 (int): The first arg

        Returns:
            Optional[str]: The return value
        """
        return arg1

    def an_instance_method(self, arg1: str) -> None:
        """An instance method

        Args:
            arg1 (str): The first arg
        """


class MockNamedTuple(NamedTuple):
    """A named tuple

    Args:
        str_arg (str): A string argument
        optional_int (Optional[int]): An optional int argument
        str_with_default (str, optional): A string argument. Defaults to 'string'.
        optional_int_with_default (Optional[int], optional): An optional int
            argument. Defaults to None.
    """
    str_arg: str
    optional_int: Optional[int]
    str_with_default: str = 'string'
    optional_int_with_default: Optional[int] = None
