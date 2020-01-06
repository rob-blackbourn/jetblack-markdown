"""Meta data"""

from __future__ import annotations
from enum import Enum, auto
import inspect
from inspect import Parameter
from typing import (
    Any,
    List,
    Optional
)

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
            arguments: List[ArgumentDescriptor],
            return_type: Optional[str],
            function_type: FunctionType,
            is_async: bool,
            summary: Optional[str],
            description: Optional[str]
    ) -> None:
        self.name = name
        self.arguments = arguments
        self.return_type = return_type
        self.function_type = function_type
        self.is_async = is_async
        self.summary = summary
        self.description = description

    @classmethod
    def create(
            cls,
            obj: Any,
            signature: inspect.Signature,
            docstring: Docstring,
            function_type: FunctionType
    ) -> FunctionDescriptor:

        is_async = inspect.iscoroutinefunction(obj) or inspect.isasyncgenfunction(obj)
        name = obj.__qualname__ if hasattr(obj, '__qualname__') else obj.__name__

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
        if signature.return_annotation and function_type != 'constructor':
            return_type = get_type_name(
                signature.return_annotation,
                docstring.returns if docstring else None
            )

        summary = docstring.short_description if docstring else None
        description = docstring.long_description if docstring else None
        return FunctionDescriptor(
            name,
            arguments,
            return_type,
            function_type,
            is_async,
            summary,
            description
        )
