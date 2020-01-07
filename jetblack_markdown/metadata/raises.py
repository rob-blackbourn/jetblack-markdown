"""Raises"""

class RaisesDescriptor:

    def __init__(
            self,
            type_: str,
            description: str
    ) -> None:
        self.type = type_
        self.description = description
