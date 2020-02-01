"""Meta data"""

from __future__ import annotations
import inspect
from types import ModuleType
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple
)

import docstring_parser

from .arguments import ArgumentDescriptor
from .common import Descriptor
from .classes import ClassDescriptor
from .callables import CallableDescriptor


class ModuleDescriptor(Descriptor):
    """A module descriptor"""

    def __init__(
            self,
            name: str,
            summary: Optional[str],
            description: Optional[str],
            attributes: List[ArgumentDescriptor],
            examples: Optional[List[str]],
            package: Optional[str],
            file: Optional[str],
            classes: List[ClassDescriptor],
            functions: List[CallableDescriptor]
    ) -> None:
        """A module descriptor

        Args:
            name (str): The module name
            summary (Optional[str]): The module summary
            description (Optional[str]): The module description
            attributes (List[ArgumentDescriptor]): The attribute list
            examples (Optional[List[str]]): Examples from the docstring
            package (Optional[str]): The package name
            file (Optional[str]): The file name
            classes (List[ClassDescriptor]): Classes in the module
            functions (List[CallableDescriptor]): Functions in the module
        """
        self.name = name
        self.summary = summary
        self.description = description
        self.attributes = attributes
        self.examples = examples
        self.package = package
        self.file = file
        self.classes = classes
        self.functions = functions

    @property
    def descriptor_type(self) -> str:
        return "module"

    def __repr__(self) -> str:
        return f'{self.name} - {self.summary}'

    @classmethod
    def create(
            cls,
            module: ModuleType,
            class_from_init: bool,
            ignore_dunder: bool,
            ignore_private: bool,
            ignore_all: bool,
            prefer_docstring: bool
    ) -> ModuleDescriptor:
        """Create a module descriptor

        Args:
            obj (Any): The module object
            class_from_init (bool): If True take the docstring from the init function
            ignore_dunder (bool): If True ignore &#95;&#95;XXX&#95;&#95; functions
            ignore_private (bool): If True ignore private methods (those prefixed &#95;XXX)
            ignore_all (bool): If True ignore the &#95;&#95;all&#95;&#95; member.
            prefer_docstring (bool): If true prefer the docstring

        Returns:
            ModuleDescriptor: A module descriptor
        """
        docstring = docstring_parser.parse(inspect.getdoc(module))

        name = module.__name__
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

        package = module.__package__
        file = module.__file__

        members: Dict[str, Any] = dict(inspect.getmembers(module))
        valid_members = members.get('__all__', [])

        classes: List[ClassDescriptor] = []
        functions: List[CallableDescriptor] = []
        for member_name, member in members.items():

            if (
                    (not ignore_all and member_name not in valid_members)
                    and inspect.getmodule(member) is not module
            ):
                # Only handler members in this module, or members in __all__ if
                # this is not ignored.
                continue
            if ignore_dunder and member_name.startswith('__') and member_name.endswith('__'):
                continue
            if ignore_private and member_name.startswith('_'):
                continue

            if ignore_all or not valid_members or member_name in valid_members:

                if inspect.isclass(member):
                    classes.append(
                        ClassDescriptor.create(
                            member,
                            class_from_init,
                            ignore_dunder,
                            ignore_private,
                            name
                        )
                    )
                elif inspect.isfunction(member):
                    functions.append(
                        CallableDescriptor.create(
                            member,
                            prefer_docstring=prefer_docstring
                        )
                    )
                else:
                    print(f'unknown {member_name}')

        print(members)

        return ModuleDescriptor(
            name,
            summary,
            description,
            attributes,
            examples,
            package,
            file,
            classes,
            functions
        )
