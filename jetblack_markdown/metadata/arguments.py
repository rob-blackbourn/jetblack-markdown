"""Arguments"""

from typing import Optional

ARG_DESCRIPTOR_EMPTY = '#EMPTY#'

class ArgumentDescriptor:

    EMPTY = ARG_DESCRIPTOR_EMPTY

    def __init__(
            self,
            name: str,
            type_: Optional[str],
            description: Optional[str],
            default: Optional[str] = ARG_DESCRIPTOR_EMPTY
    ) -> None:
        self.name = name
        self.type = type_
        self.description = description
        self.default = default

    @property
    def is_optional(self) -> bool:
        return self.default is ArgumentDescriptor.EMPTY
