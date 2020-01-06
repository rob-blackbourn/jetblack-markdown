"""Meta data"""

from __future__ import annotations
from enum import Enum, auto
import inspect
from inspect import Parameter
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple
)

import docstring_parser
from docstring_parser import Docstring

from .utils import (
    find_docstring_param,
    get_type_name
)

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

class RaisesDescriptor:

    def __init__(
            self,
            type_: str,
            description: str
    ) -> None:
        self.type = type_
        self.description = description

class FunctionType(Enum):
    FUNCTION = auto()
    METHOD = auto()
    CONSTRUCTOR = auto()

class FunctionDescriptor:

    POSITIONAL_ONLY = '/'
    KEYWORD_ONLY = '*'

    def __init__(
            self,
            name: str,
            summary: Optional[str],
            description: Optional[str],
            arguments: List[ArgumentDescriptor],
            return_type: Optional[str],
            return_description: Optional[str],
            function_type: FunctionType,
            is_async: bool,
            is_generator: bool,
            raises: Optional[List[RaisesDescriptor]],
            examples: Optional[List[str]],
            module: str,
            package: Optional[str],
            file: Optional[str]
    ) -> None:
        self.name = name
        self.summary = summary
        self.description = description
        self.arguments = arguments
        self.return_type = return_type
        self.return_description = return_description
        self.function_type = function_type
        self.is_async = is_async
        self.is_generator = is_generator
        self.raises = raises
        self.examples = examples
        self.module = module
        self.package = package
        self.file = file

    @property
    def function_type_name(self) -> str:
        if self.function_type == FunctionType.CONSTRUCTOR:
            return 'class'
        elif self.function_type == FunctionType.METHOD:
            return 'method'
        elif self.is_generator:
            if self.is_async:
                return 'async generator function'
            else:
                return 'generator function'
        else:
            return 'function'

    @classmethod
    def create(
            cls,
            obj: Any,
            signature: inspect.Signature,
            docstring: Docstring,
            function_type: FunctionType
    ) -> FunctionDescriptor:

        name = obj.__qualname__ if hasattr(obj, '__qualname__') else obj.__name__
        is_async = inspect.iscoroutinefunction(obj) or inspect.isasyncgenfunction(obj)
        is_generator = inspect.isgeneratorfunction(obj) or inspect.isasyncgenfunction(obj)

        arguments: List[ArgumentDescriptor] = []
        is_pos_only_rendered = False
        is_kw_only_rendered = False
        is_self = function_type in {'method', 'constructor'}
        for parameter in signature.parameters.values():
            if is_self:
                is_self = False
                continue

            if parameter.kind is Parameter.VAR_POSITIONAL:
                arg_name = '*' + parameter.name
                type_name = None
                default = ArgumentDescriptor.EMPTY
            elif parameter.kind is Parameter.VAR_KEYWORD:
                arg_name = '**' + parameter.name
                type_name = None
                default = ArgumentDescriptor.EMPTY
            else:
                if parameter.kind is Parameter.POSITIONAL_ONLY and not is_pos_only_rendered:
                    arguments.append(
                        ArgumentDescriptor(
                            FunctionDescriptor.POSITIONAL_ONLY,
                            None,
                            None
                        )
                    )
                    is_pos_only_rendered = True
                elif parameter.kind is Parameter.KEYWORD_ONLY and not is_kw_only_rendered:
                    arguments.append(
                        ArgumentDescriptor(
                            FunctionDescriptor.KEYWORD_ONLY,
                            None,
                            None
                        )
                    )
                    is_kw_only_rendered = True

                arg_name = parameter.name

                docstring_param = find_docstring_param(
                    parameter.name,
                    docstring
                )

                type_name = get_type_name(parameter.annotation, docstring_param)

                default = parameter.default if parameter.default != Parameter.empty else ArgumentDescriptor.EMPTY

            description = docstring_param.description if docstring_param else None

            arguments.append(
                ArgumentDescriptor(arg_name, type_name, description, default)
            )

        return_type: Optional[str] = None
        return_description: Optional[str] = None
        if signature.return_annotation and function_type != FunctionType.CONSTRUCTOR:
            return_type = get_type_name(
                signature.return_annotation,
                docstring.returns if docstring else None
            )
            return_description = docstring.returns.description if docstring and docstring.returns else None

        raises: Optional[List[RaisesDescriptor]] = [
            RaisesDescriptor(error.type_name, error.description)
            for error in docstring.raises
        ] if docstring and docstring.raises else None

        summary = docstring.short_description if docstring else None
        description = docstring.long_description if docstring else None

        examples: Optional[List[str]] = [
            meta.description
            for meta in docstring.meta
            if 'examples' in meta.args
        ] if docstring is not None else None


        module_obj = inspect.getmodule(obj)
        module = obj.__module__
        package = module_obj.__package__ if module_obj else None
        file = module_obj.__file__ if module_obj else None

        return FunctionDescriptor(
            name,
            summary,
            description,
            arguments,
            return_type,
            return_description,
            function_type,
            is_async,
            is_generator,
            raises,
            examples,
            module,
            package,
            file
        )

class PropertyDescriptor:

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
        self.name = name
        self.qual_name = qual_name
        self.summary = summary
        self.description = description
        self.type = type_
        self.is_settable = is_settable
        self.is_deletable = is_deletable
        self.raises = raises
        self.examples = examples

    @classmethod
    def create(
            cls,
            obj: Any,
            klass: Any,
            property_name: str
    ) -> PropertyDescriptor:
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
        type_name = get_type_name(signature.return_annotation, docstring.returns)
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

class ClassDescriptor:

    def __init__(
            self,
            name: str,
            summary: Optional[str],
            description: Optional[str],
            constructor: FunctionDescriptor,
            attributes: List[ArgumentDescriptor],
            properties: List[PropertyDescriptor],
            methods: List[FunctionDescriptor],
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
        constructor = FunctionDescriptor.create(
            obj,
            signature,
            docstring,
            FunctionType.CONSTRUCTOR
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
        methods: List[FunctionDescriptor] = []
        for name, member in members.items():
            if name == '__init__' or (
                    ignore_dunder and
                    name.startswith('__') and
                    name.endswith('__')
            ) or (ignore_private and name.startswith('_')):
                continue

            if member.__class__ is property:
                properties.append(
                    PropertyDescriptor.create(
                        member,
                        obj,
                        name
                    )
                )
            elif inspect.isfunction(member):
                method_signature = inspect.signature(member)
                method_docstring = docstring_parser.parse(inspect.getdoc(member))
                methods.append(
                    FunctionDescriptor.create(
                        member,
                        method_signature,
                        method_docstring,
                        FunctionType.METHOD
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

class ModuleDescriptor:

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
