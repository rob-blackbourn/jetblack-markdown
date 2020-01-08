"""Callables"""

from __future__ import annotations
from enum import Enum, auto
import inspect
from inspect import Parameter, Signature
from typing import (
    Any,
    List,
    Optional
)

import docstring_parser
from docstring_parser import Docstring

from ..utils import (
    find_docstring_param,
    get_type_name
)

from .arguments import ArgumentDescriptor
from .common import Descriptor
from .raises import RaisesDescriptor


class CallableType(Enum):
    """An enum indicating the type of a callable"""
    FUNCTION = auto()
    METHOD = auto()
    CONSTRUCTOR = auto()


class CallableDescriptor(Descriptor):
    """A descriptor for a callable"""

    POSITIONAL_ONLY = '/'
    KEYWORD_ONLY = '*'

    def __init__(
            self,
            name: str,
            summary: Optional[str],
            description: Optional[str],
            arguments: List[ArgumentDescriptor],
            return_type: str,
            return_description: Optional[str],
            function_type: CallableType,
            is_async: bool,
            is_generator: bool,
            raises: Optional[List[RaisesDescriptor]],
            examples: Optional[List[str]],
            module: str,
            package: Optional[str],
            file: Optional[str]
    ) -> None:
        """A descriptor for a callable

        Args:
            name (str): The name of the callable
            summary (Optional[str]): The callables summary docstring
            description (Optional[str]): The callables description docstring
            arguments (List[ArgumentDescriptor]): The callables arguments
            return_type (str): The callables return type
            return_description (Optional[str]): The callables return description
            function_type (CallableType): The type of callable
            is_async (bool): True if the callable is async
            is_generator (bool): True if the callable is a generator
            raises (Optional[List[RaisesDescriptor]]): A list of the exceptions
                raised
            examples (Optional[List[str]]): A list of examples
            module (str): The module name
            package (Optional[str]): The package name
            file (Optional[str]): The file name
        """
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
    def descriptor_type(self) -> str:
        return "callable"

    @property
    def function_type_name(self) -> str:
        """The function type name.

        One of: 'class', 'method', 'async generator function'
        'generator function', 'function'

        Returns:
            str: The function type name
        """
        if self.function_type == CallableType.CONSTRUCTOR:
            return 'class'
        elif self.function_type == CallableType.METHOD:
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
            signature: Optional[Signature] = None,
            docstring: Optional[Docstring] = None,
            function_type: CallableType = CallableType.FUNCTION
    ) -> CallableDescriptor:
        """Create a callable descriptor from a callable

        Args:
            obj (Any): The callable
            signature (Optional[Signature], optional): The signature. Defaults
                to None.
            docstring (Optional[Docstring], optional): The docstring. Defaults
                to None.
            function_type (CallableType, optional): The function type. Defaults
                to CallableType.FUNCTION.

        Returns:
            CallableDescriptor: A callable descriptor
        """
        if signature is None:
            signature = inspect.signature(obj)
        if docstring is None:
            docstring = docstring_parser.parse(inspect.getdoc(obj))

        name = obj.__qualname__ if hasattr(
            obj, '__qualname__') else obj.__name__
        is_async = inspect.iscoroutinefunction(
            obj) or inspect.isasyncgenfunction(obj)
        is_generator = inspect.isgeneratorfunction(
            obj) or inspect.isasyncgenfunction(obj)

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
                docstring_param = None
            elif parameter.kind is Parameter.VAR_KEYWORD:
                arg_name = '**' + parameter.name
                type_name = None
                default = ArgumentDescriptor.EMPTY
                docstring_param = None
            else:
                if parameter.kind is Parameter.POSITIONAL_ONLY and not is_pos_only_rendered:
                    arguments.append(
                        ArgumentDescriptor(
                            CallableDescriptor.POSITIONAL_ONLY,
                            None,
                            None
                        )
                    )
                    is_pos_only_rendered = True
                elif parameter.kind is Parameter.KEYWORD_ONLY and not is_kw_only_rendered:
                    arguments.append(
                        ArgumentDescriptor(
                            CallableDescriptor.KEYWORD_ONLY,
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

                type_name = get_type_name(
                    parameter.annotation, docstring_param)

                default = (
                    parameter.default
                    if parameter.default != Parameter.empty
                    else ArgumentDescriptor.EMPTY
                )

            description = (
                docstring_param.description
                if docstring_param
                else None
            )

            arguments.append(
                ArgumentDescriptor(arg_name, type_name, description, default)
            )

        return_description: Optional[str] = None
        if function_type == CallableType.CONSTRUCTOR:
            return_type = 'None'
        elif not signature.return_annotation:
            return_type = 'Any'
        else:
            return_type = get_type_name(
                signature.return_annotation,
                docstring.returns if docstring else None
            )
            return_description = (
                docstring.returns.description
                if docstring and docstring.returns
                else None
            )

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

        return CallableDescriptor(
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
