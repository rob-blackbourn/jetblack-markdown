"""Raises"""

from .common import Descriptor


class RaisesDescriptor(Descriptor):

    def __init__(
            self,
            type_: str,
            description: str
    ) -> None:
        self.type = type_
        self.description = description

    @property
    def descriptor_type(self) -> str:
        return "raises"
