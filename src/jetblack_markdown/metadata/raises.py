"""Raises"""

from .common import Descriptor


class RaisesDescriptor(Descriptor):
    """A raises descriptor"""

    def __init__(
            self,
            type_: str,
            description: str
    ) -> None:
        """A raises descriptor

        Args:
            type_ (str): The type of exception raised
            description (str): The exception description
        """
        self.type = type_
        self.description = description

    @property
    def descriptor_type(self) -> str:
        return "raises"

    def __repr__(self) -> str:
        return f'{self.type} - {self.description}'
