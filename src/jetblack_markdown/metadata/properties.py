"""Properties"""

from __future__ import annotations

import inspect
from typing import Any

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
            summary: str | None,
            description: str | None,
            type_: str | None,
            is_settable: bool,
            is_deletable: bool,
            raises: list[RaisesDescriptor] | None,
            examples: list[str] | None
    ) -> None:
        """A properties descriptor

        Args:
            qualifier (str): The qualifier
            name (str): The property name
            summary (str | None): The summary from the docstring
            description (str | None): The description from the docstring
            type_ (str | None): The property type
            is_settable (bool): If True the property can be set
            is_deletable (bool): If True the property can be deleted
            raises (list[RaisesDescriptor] | None): A list of the exceptions
                the property might raise.
            examples (list[str] | None): A list of examples from the
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
            docstring = docstring_parser.parse(inspect.getdoc(klass) or '')
            docstring_param = find_docstring_param(name, docstring)
            field_type = klass._field_types[name]  # pylint: disable=protected-access
            type_name = get_type_name(
                field_type,
                docstring_param
            )
            summary = docstring_param.description if docstring_param else None
            description: str | None = None
            raises: list[RaisesDescriptor] | None = None
            is_settable = False
            is_deletable = False
            examples: list[str] | None = None
        else:
            docstring = docstring_parser.parse(inspect.getdoc(obj) or '')
            signature = inspect.signature(obj.fget)
            type_name = get_type_name(
                signature.return_annotation,
                docstring.returns
            )
            summary = docstring.short_description if docstring else None
            description = docstring.long_description if docstring else None
            raises = [
                RaisesDescriptor(
                    error.type_name or '',
                    error.description or ''
                )
                for error in docstring.raises
            ] if docstring and docstring.raises else None

            is_settable = 'fset' in members and members['fset']
            is_deletable = 'fdel' in members and members['fdel']
            examples = [
                meta.description or ''
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
