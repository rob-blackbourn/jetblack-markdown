"""Classes"""

from __future__ import annotations
import inspect
from typing import (
    Any,
    Dict,
    List,
    Optional
)

import docstring_parser

from .arguments import ArgumentDescriptor
from .callables import CallableDescriptor, CallableType
from .common import Descriptor
from .properties import PropertyDescriptor


class ClassDescriptor(Descriptor):
    """A class descriptor"""

    def __init__(
            self,
            name: str,
            summary: Optional[str],
            description: Optional[str],
            constructor: CallableDescriptor,
            attributes: List[ArgumentDescriptor],
            properties: List[PropertyDescriptor],
            class_methods: List[CallableDescriptor],
            methods: List[CallableDescriptor],
            examples: Optional[List[str]],
            module: str,
            package: Optional[str],
            file: Optional[str]
    ) -> None:
        """A class descriptor

        Args:
            name (str): The class name
            summary (Optional[str]): The docstring summary
            description (Optional[str]): The docstring description
            constructor (CallableDescriptor): The constructor
            attributes (List[ArgumentDescriptor]): The class attributes
            properties (List[PropertyDescriptor]): The class properties
            class_methods (List[CallableDescriptor]): The class methods
            methods (List[CallableDescriptor]): The class methods
            examples (Optional[List[str]]): Examples from the docstring
            module (str): The module
            package (Optional[str]): The package
            file (Optional[str]): The file
        """
        self.name = name
        self.summary = summary
        self.description = description
        self.constructor = constructor
        self.attributes = attributes
        self.properties = properties
        self.class_methods = class_methods
        self.methods = methods
        self.examples = examples
        self.module = module
        self.package = package
        self.file = file

    @property
    def descriptor_type(self) -> str:
        return "class"

    @classmethod
    def create(
            cls,
            obj: Any,
            class_from_init: bool,
            ignore_dunder: bool,
            ignore_private: bool,
    ) -> ClassDescriptor:
        """Create a class

        Args:
            obj (Any): The class
            class_from_init (bool): If True take the docstring from the init function
            ignore_dunder (bool): If True ignore &#95;&#95;XXX&#95;&#95; functions
            ignore_private (bool): If True ignore private methods (those prefixed &#95;XXX)

        Returns:
            ClassDescriptor: The class descriptor
        """
        members: Dict[str, Any] = {
            name: value
            for name, value in inspect.getmembers(obj)
        }
        signature = inspect.signature(obj)
        docstring = docstring_parser.parse(
            inspect.getdoc(
                members['__init__'] if class_from_init else obj
            )
        )
        name = obj.__qualname__ if hasattr(
            obj, '__qualname__') else obj.__name__
        summary = docstring.short_description if docstring else None
        description = docstring.long_description if docstring else None
        constructor = CallableDescriptor.create(
            obj,
            signature,
            docstring,
            CallableType.CONSTRUCTOR
        )
        attributes: List[ArgumentDescriptor] = []
        if docstring:
            attrs = [
                (meta.args[1], meta.description)
                for meta in docstring.meta
                if 'attribute' in meta.args
            ]
            for attr_details, attr_desc in attrs:
                attr_name, _sep, attr_type = attr_details.partition(' ')
                attr_type = attr_type.strip('()')
                attributes.append(
                    ArgumentDescriptor(attr_name, attr_type, attr_desc)
                )
        properties: List[PropertyDescriptor] = []
        methods: List[CallableDescriptor] = []
        class_methods: List[CallableDescriptor] = []
        for member_name, member in members.items():
            if member_name == '__init__' or (
                    ignore_dunder and
                    member_name.startswith('__') and
                    member_name.endswith('__')
            ) or (ignore_private and member_name.startswith('_')):
                continue

            if member.__class__ is property:
                properties.append(
                    PropertyDescriptor.create(
                        member,
                        obj,
                        member_name
                    )
                )
            elif inspect.isfunction(member):
                # Instance methods
                methods.append(
                    CallableDescriptor.create(
                        member,
                        function_type=CallableType.METHOD
                    )
                )
            elif inspect.ismethod(member):
                # Class methods
                class_methods.append(
                    CallableDescriptor.create(
                        member,
                        function_type=CallableType.CLASS_METHOD
                    )
                )

        examples: Optional[List[str]] = [
            meta.description
            for meta in docstring.meta
            if 'examples' in meta.args
        ] if docstring is not None else None

        module_obj = inspect.getmodule(obj)
        module = obj.__module__
        package = module_obj.__package__ if module_obj else None
        file = module_obj.__file__ if module_obj else None

        return ClassDescriptor(
            name,
            summary,
            description,
            constructor,
            attributes,
            properties,
            class_methods,
            methods,
            examples,
            module,
            package,
            file
        )
