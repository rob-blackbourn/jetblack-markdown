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
from .properties import PropertyDescriptor

class ClassDescriptor:

    def __init__(
            self,
            name: str,
            summary: Optional[str],
            description: Optional[str],
            constructor: CallableDescriptor,
            attributes: List[ArgumentDescriptor],
            properties: List[PropertyDescriptor],
            methods: List[CallableDescriptor],
            examples: Optional[List[str]],
            module: str,
            package: Optional[str],
            file: Optional[str]
    ) -> None:
        self.name = name
        self.summary = summary
        self.description = description
        self.constructor = constructor
        self.attributes = attributes
        self.properties = properties
        self.methods = methods
        self.examples = examples
        self.module = module
        self.package = package
        self.file = file

    @classmethod
    def create(
            cls,
            obj: Any,
            class_from_init: bool,
            ignore_dunder: bool,
            ignore_private: bool,
    ) -> ClassDescriptor:
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
        name = obj.__qualname__ if hasattr(obj, '__qualname__') else obj.__name__
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
                method_signature = inspect.signature(member)
                method_docstring = docstring_parser.parse(inspect.getdoc(member))
                methods.append(
                    CallableDescriptor.create(
                        member,
                        method_signature,
                        method_docstring,
                        CallableType.METHOD
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
            methods,
            examples,
            module,
            package,
            file
        )
