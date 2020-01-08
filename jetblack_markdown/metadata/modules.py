"""Meta data"""

from __future__ import annotations
import inspect
from typing import (
    Any,
    List,
    Optional,
    Tuple
)

import docstring_parser

from .arguments import ArgumentDescriptor
from .common import Descriptor


class ModuleDescriptor(Descriptor):

    def __init__(
            self,
            name: str,
            summary: Optional[str],
            description: Optional[str],
            attributes: List[ArgumentDescriptor],
            examples: Optional[List[str]],
            package: str,
            file: str
    ) -> None:
        self.name = name
        self.summary = summary
        self.description = description
        self.attributes = attributes
        self.examples = examples
        self.package = package
        self.file = file

    @property
    def descriptor_type(self) -> str:
        return "module"


    @classmethod
    def create(
        cls,
        obj: Any
    ) -> ModuleDescriptor:
        docstring = docstring_parser.parse(inspect.getdoc(obj))

        name = obj.__qualname__ if hasattr(obj, '__qualname__') else obj.__name__
        summary = docstring.short_description if docstring else None
        description = docstring.short_description if docstring else None
        attrs: List[Tuple[str, str]] = [
            (meta.args[1], meta.description)
            for meta in docstring.meta
            if 'attribute' in meta.args
        ]
        attributes: List[ArgumentDescriptor] = []
        for attr_details, attr_desc in attrs:
            attr_name, _sep, attr_type = attr_details.partition(' ')
            attr_type = attr_type.strip('()')
            attributes.append(
                ArgumentDescriptor(attr_name, attr_type, attr_desc)
            )
        examples: Optional[List[str]] = [
            meta.description
            for meta in docstring.meta
            if 'examples' in meta.args
        ] if docstring is not None else None

        package = obj.__package__
        file = obj.__file__

        return ModuleDescriptor(
            name,
            summary,
            description,
            attributes,
            examples,
            package,
            file
        )
