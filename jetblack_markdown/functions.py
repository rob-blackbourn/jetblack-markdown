"""Rendering functions
"""

from __future__ import annotations
import inspect
from typing import (
    Any,
    List,
    Optional
)

import docstring_parser
from markdown import Markdown
from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .utils import (
    create_subelement,
    create_span_subelement,
    create_text_subelement
)

from .renderers import (
    render_title,
    render_summary,
    render_description,
    render_examples,
    render_meta_data
)

from .metadata import (
    ArgumentDescriptor,
    FunctionType,
    FunctionDescriptor,
    RaisesDescriptor
)

def _render_signature(
        function_descriptor: FunctionDescriptor,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'code',
        [('class', f'{HTML_CLASS_BASE}-function-signature')],
        parent
    )

    if function_descriptor.is_async:
        create_span_subelement(
            "async ",
            f'{HTML_CLASS_BASE}-function-punctuation',
            container
        )

    create_span_subelement(
        function_descriptor.name,
        f'{HTML_CLASS_BASE}-function-name',
        container
    )

    create_span_subelement('(', f'{HTML_CLASS_BASE}-punctuation', container)

    is_first = True
    for argument in function_descriptor.arguments:
        if is_first:
            is_first = False
        else:
            create_span_subelement(
                ', ',
                f'{HTML_CLASS_BASE}-punctuation',
                container
            )

        create_text_subelement(
            'var',
            argument.name,
            f'{HTML_CLASS_BASE}-function-var',
            container
        )

        if argument.type:
            create_span_subelement(
                ': ', f'{HTML_CLASS_BASE}-punctuation', container)
            create_span_subelement(
                argument.type,
                f'{HTML_CLASS_BASE}-variable-type',
                container
            )

    create_span_subelement(')', f'{HTML_CLASS_BASE}-punctuation', container)

    if function_descriptor.return_type:
        create_span_subelement(
            ' -> ', f'{HTML_CLASS_BASE}-punctuation', container)
        create_span_subelement(
            function_descriptor.return_type,
            f'{HTML_CLASS_BASE}-variable-type',
            container
        )


def _render_parameters(
        arguments: List[ArgumentDescriptor],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-parameters')],
        parent
    )
    create_text_subelement(
        'h3',
        'Parameters',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    for argument in arguments:

        parameter_container = create_subelement(
            'div',
            [('class', f'{HTML_CLASS_BASE}-function-parameters')],
            container
        )

        create_text_subelement(
            'var',
            argument.name,
            f'{HTML_CLASS_BASE}-function-var',
            parameter_container
        )

        if argument.type:
            create_span_subelement(
                ': ',
                f'{HTML_CLASS_BASE}-punctuation',
                parameter_container
            )
            create_span_subelement(
                argument.type,
                f'{HTML_CLASS_BASE}-variable-type',
                parameter_container
            )

        if argument.is_optional:
            create_span_subelement(
                ' (optional)',
                f'{HTML_CLASS_BASE}-punctuation',
                parameter_container
            )


        create_subelement('br', [], parameter_container)

        create_text_subelement(
            'p',
            md.convert(argument.description or ''),
            f'{HTML_CLASS_BASE}-function-param',
            parameter_container
        )

    return container


def _render_returns(
        function_descriptor: FunctionDescriptor,
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-function-returns')],
        parent
    )

    if not function_descriptor.return_type or function_descriptor.return_type in ('None', 'typing.None'):
        return container

    create_text_subelement(
        'h3',
        'Yields' if function_descriptor.is_generator else 'Returns',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    create_span_subelement(
        function_descriptor.return_type,
        f'{HTML_CLASS_BASE}-variable-type',
        container
    )
    create_span_subelement(
        ': ',
        f'{HTML_CLASS_BASE}-punctuation',
        container
    )

    description = function_descriptor.return_description or ''
    text = md.convert(description)
    if text.startswith('<p>') and text.endswith('</p>'):
        text = text[3:-4]
    create_span_subelement(
        text,
        f'{HTML_CLASS_BASE}-description',
        container
    )

    return container


def _render_raises(
        raises: Optional[List[RaisesDescriptor]],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-raises')],
        parent
    )
    if not raises:
        return container

    create_text_subelement(
        'h3',
        'Raises',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    for error in raises:
        error_container = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-function-raises')],
            container
        )

        create_span_subelement(
            error.type,
            f'{HTML_CLASS_BASE}-variable-type',
            error_container
        )
        create_span_subelement(
            ': ',
            f'{HTML_CLASS_BASE}-punctuation',
            error_container
        )

        text = md.convert(error.description)
        if text.startswith('<p>') and text.endswith('</p>'):
            text = text[3:-4]
        create_span_subelement(
            text,
            f'{HTML_CLASS_BASE}-function-raises',
            error_container
        )

    return container


def get_function_type(function_descriptor: FunctionDescriptor) -> str:
    if function_descriptor.function_type == FunctionType.CONSTRUCTOR:
        return 'class'
    elif function_descriptor.function_type == FunctionType.METHOD:
        return 'method'
    elif function_descriptor.is_generator:
        if function_descriptor.is_async:
            return 'async generator function'
        else:
            return 'generator function'
    else:
        return 'function'

def create_function(
        function_descriptor: FunctionDescriptor,
        md: Markdown,
        container: etree.Element
) -> etree.Element:

    function_type = get_function_type(function_descriptor)
    render_title(function_descriptor.name, function_type, container)
    render_meta_data(function_descriptor.module, function_descriptor.package, function_descriptor.file, container)
    render_summary(function_descriptor.summary, container, md)
    _render_signature(function_descriptor, container)
    _render_parameters(function_descriptor.arguments, container, md)
    _render_returns(function_descriptor, container, md)
    _render_raises(function_descriptor.raises, container, md)
    render_description(function_descriptor.description, container, md)
    render_examples(function_descriptor.examples, container, md)

    return container

def render_function(
        obj: Any,
        md: Markdown,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-function')],
        parent
    )

    signature = inspect.signature(obj)
    docstring = docstring_parser.parse(inspect.getdoc(obj))

    function_descriptor = FunctionDescriptor.create(
        obj,
        signature,
        docstring,
        FunctionType.FUNCTION
    )

    return create_function(function_descriptor, md, container)

