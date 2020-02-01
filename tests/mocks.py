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
