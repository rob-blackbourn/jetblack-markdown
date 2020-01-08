"""Properties"""

from __future__ import annotations
import inspect
from typing import (
    Any,
    List,
    Optional
)

import docstring_parser

from ..utils import get_type_name

from .common import Descriptor
from .raises import RaisesDescriptor


class PropertyDescriptor(Descriptor):
    """A properties descriptor"""

    def __init__(
            self,
            name: str,
            qual_name: str,
            summary: Optional[str],
            description: Optional[str],
            type_: Optional[str],
            is_settable: bool,
            is_deletable: bool,
            raises: Optional[List[RaisesDescriptor]],
            examples: Optional[List[str]]
    ) -> None:
        """A properties descriptor

        Args:
            name (str): The property name
            qual_name (str): The property qualified name
            summary (Optional[str]): The summary from the docstring
            description (Optional[str]): The description from the docstring
            type_ (Optional[str]): The property type
            is_settable (bool): If True the property can be set
            is_deletable (bool): If True the property can be deleted
            raises (Optional[List[RaisesDescriptor]]): A list of the exceptions
                the property might raise.
            examples (Optional[List[str]]): A list of examples from the
                docstring
        """
        self.name = name
        self.qual_name = qual_name
        self.summary = summary
        self.description = description
        self.type = type_ or 'Any'
        self.is_settable = is_settable
        self.is_deletable = is_deletable
        self.raises = raises
        self.examples = examples

    @property
    def descriptor_type(self) -> str:
        return "property"

    @classmethod
    def create(
            cls,
            obj: Any,
            klass: Any,
            property_name: str
    ) -> PropertyDescriptor:
        """Create a property descriptor from

        Args:
            obj (Any): The property object
            klass (Any): The class object
            property_name (str): The name of the property

        Returns:
            PropertyDescriptor: A property descriptor
        """
        signature = inspect.signature(obj.fget)
        docstring = docstring_parser.parse(inspect.getdoc(obj))
        members = {
            name
            for name, _value in inspect.getmembers(obj)
        }

        name = property_name
        qual_name = klass.__name__ + '.' + property_name
        summary = docstring.short_description if docstring else None
        description = docstring.long_description if docstring else None
        type_name = get_type_name(
            signature.return_annotation, docstring.returns)
        is_settable = 'fset' in members
        is_deletable = 'fdel' in members
        raises: Optional[List[RaisesDescriptor]] = [
            RaisesDescriptor(error.type_name, error.description)
            for error in docstring.raises
        ] if docstring and docstring.raises else None
        examples: Optional[List[str]] = [
            meta.description
            for meta in docstring.meta
            if 'examples' in meta.args
        ] if docstring is not None else None

        return PropertyDescriptor(
            name,
            qual_name,
            summary,
            description,
            type_name,
            is_settable,
            is_deletable,
            raises,
            examples
        )
