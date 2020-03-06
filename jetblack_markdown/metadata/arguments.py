"""Arguments"""

from typing import Optional

from .common import Descriptor

ARG_DESCRIPTOR_EMPTY = '#EMPTY#'


class ArgumentDescriptor(Descriptor):
    """A descriptor for arguments"""

    EMPTY = ARG_DESCRIPTOR_EMPTY

    def __init__(
            self,
            name: str,
            type_: Optional[str],
            description: Optional[str],
            default: Optional[str] = ARG_DESCRIPTOR_EMPTY
    ) -> None:
        """A descriptor for arguments

        Args:
            name (str): The argument name
            type_ (Optional[str]): The argument type
            description (Optional[str]): The arguments description
            default (Optional[str], optional): The default value. Defaults to ARG_DESCRIPTOR_EMPTY.
        """
        self.name = name
        self.type = type_
        self.description = description
        self.default = default

    @property
    def is_optional(self) -> bool:
        """Indicates whether the argument is optional

        Note that an argument is optional if it has a default value, not if it
        has the Optional[...] type decoration.

        Returns:
            bool: True if the argument is optional
        """
        return self.default is not ArgumentDescriptor.EMPTY

    @property
    def descriptor_type(self) -> str:
        return "argument"

    def __repr__(self):
        return f'{self.name}: {self.type} - {self.description}'
