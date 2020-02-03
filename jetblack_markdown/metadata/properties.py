"""Properties"""

from __future__ import annotations
import inspect
from typing import (
    Any,
    List,
    Optional
)

import docstring_parser

from ..utils import get_type_name, find_docstring_param

from .common import Descriptor
from .raises import RaisesDescriptor
from .utils import is_named_tuple_type


class PropertyDescriptor(Descriptor):
    """A properties descriptor"""

    def __init__(
            self,
            qualifier: str,
            name: str,
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
            qualifier (str): The qualifier
            name (str): The property name
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
        self.qualifier = qualifier
        self.name = name
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

    def __repr__(self) -> str:
        return f'{self.name} - {self.summary}'

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
        members = {
            name: value
            for name, value in inspect.getmembers(obj)
        }

        name = property_name
        qualifier = klass.__name__

        if is_named_tuple_type(klass) and name in klass._fields:
            docstring = docstring_parser.parse(inspect.getdoc(klass))
            docstring_param = find_docstring_param(name, docstring)
            field_type = klass._field_types[name] # pylint: disable=protected-access
            type_name = get_type_name(
                field_type,
                docstring_param
            )
            summary = docstring_param.description if docstring_param else None
            description: Optional[str] = None
            raises: Optional[List[RaisesDescriptor]] = None
            is_settable = False
            is_deletable = False
            examples: Optional[List[str]] = None
        else:
            docstring = docstring_parser.parse(inspect.getdoc(obj))
            signature = inspect.signature(obj.fget)
            type_name = get_type_name(
                signature.return_annotation,
                docstring.returns
            )
            summary = docstring.short_description if docstring else None
            description = docstring.long_description if docstring else None
            raises = [
                RaisesDescriptor(error.type_name, error.description)
                for error in docstring.raises
            ] if docstring and docstring.raises else None

            is_settable = 'fset' in members and members['fset']
            is_deletable = 'fdel' in members and members['fdel']
            examples = [
                meta.description
                for meta in docstring.meta
                if 'examples' in meta.args
            ] if docstring is not None else None

        return PropertyDescriptor(
            qualifier,
            name,
            summary,
            description,
            type_name,
            is_settable,
            is_deletable,
            raises,
            examples
        )
