"""Common code for metadata"""

from abc import ABCMeta, abstractmethod


class Descriptor(metaclass=ABCMeta):
    """The descriptor base class"""

    @property
    @abstractmethod
    def descriptor_type(self) -> str:
        """The descriptor type

        Returns:
            str: The type of the descriptor
        """
