"""Rendering functions
"""

import inspect
import typing
from typing import (
    Any,
    List,
    Optional,
    Set
)

import docstring_parser
from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .utils import create_subelement, create_span_subelement, create_text_subelement


def _render_function_title(obj: Any, parent: etree.Element) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-title')],
        parent
    )

    header = create_subelement(
        'h1',
        [('class', f'{HTML_CLASS_BASE}-function-header')],
        container
    )

    create_span_subelement(
        obj.__name__,
        f'{HTML_CLASS_BASE}-function-name',
        header
    )
    create_span_subelement(
        ' ',
        None,
        header
    )
    create_span_subelement(
        '(function)',
        f'{HTML_CLASS_BASE}-object-type',
        header
    )

    return container


def _render_meta_data(obj: Any, parent: etree.Element) -> etree.Element:
    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-metadata')],
        parent
    )

    create_text_subelement(
        'strong',
        'Module:',
        f'{HTML_CLASS_BASE}-metadata-header',
        container
    )
    create_span_subelement(
        ' ',
        None,
        container
    )
    create_span_subelement(
        obj.__module__,
        f'{HTML_CLASS_BASE}-metadata-value',
        container
    )
    create_subelement('br', [], container)

    module = inspect.getmodule(obj)
    if module is not None:
        if module.__package__:
            create_text_subelement(
                'strong',
                'Package: ',
                f'{HTML_CLASS_BASE}-metadata-header',
                container
            )
            create_span_subelement(
                ' ',
                None,
                container
            )
            create_span_subelement(
                module.__package__,
                f'{HTML_CLASS_BASE}-metadata-value',
                container
            )
            create_subelement('br', [], container)

        if module.__file__:
            create_text_subelement(
                'strong',
                'File',
                f'{HTML_CLASS_BASE}-metadata-header',
                container
            )
            create_span_subelement(
                ': ',
                None,
                container
            )
            create_span_subelement(
                module.__file__,
                f'{HTML_CLASS_BASE}-metadata-value',
                container
            )
            create_subelement('br', [], container)

    return container


def _render_summary(
        docstring: Optional[docstring_parser.Docstring],
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-summary')],
        parent
    )

    if docstring and docstring.short_description:
        summary = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-function-summary')],
            container
        )
        summary.text = docstring.short_description

    return container


def _get_type_name(
        annotation: Any,
        docstring_param: Optional[docstring_parser.DocstringParam]
) -> str:
    type_name = docstring_param.type_name if docstring_param else None
    if not type_name:
        type_name = getattr(annotation, '__name__', None)
    if not type_name:
        type_name = getattr(annotation, '_', None)
    if not type_name:
        type_name = str(annotation)
    return type_name


def _get_return_type_name(
        annotation: Any,
        docstring_returns: Optional[docstring_parser.DocstringReturns]
) -> str:
    type_name = docstring_returns.type_name if docstring_returns else None
    if not type_name:
        type_name = getattr(annotation, '__name__', None)
    if not type_name:
        type_name = getattr(annotation, '_', None)
    if not type_name:
        type_name = str(annotation)
    return type_name


def _render_signature(
        obj: Any,
        signature: inspect.Signature,
        docstring: docstring_parser.Docstring,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-function-signature')],
        parent
    )

    create_span_subelement(
        obj.__name__,
        f'{HTML_CLASS_BASE}-function-name',
        container
    )

    create_span_subelement('(', f'{HTML_CLASS_BASE}-punctuation', container)

    for index, parameter in enumerate(signature.parameters.values()):
        if index:
            create_span_subelement(
                ', ', f'{HTML_CLASS_BASE}-punctuation', container)
        create_text_subelement(
            'var',
            parameter.name,
            f'{HTML_CLASS_BASE}-function-var',
            container
        )
        if parameter.annotation:

            docstring_param = next(
                param
                for param in docstring.params
                if param.arg_name == parameter.name
            ) if docstring else None

            type_name = _get_type_name(parameter.annotation, docstring_param)

            create_span_subelement(
                ': ', f'{HTML_CLASS_BASE}-punctuation', container)
            create_span_subelement(
                type_name,
                f'{HTML_CLASS_BASE}-variable-type',
                container
            )

    create_span_subelement(')', f'{HTML_CLASS_BASE}-punctuation', container)

    if signature.return_annotation:
        type_name = _get_return_type_name(
            signature.return_annotation,
            docstring.returns if docstring else None
        )

        create_span_subelement(
            ' -> ', f'{HTML_CLASS_BASE}-punctuation', container)
        create_span_subelement(
            type_name,
            f'{HTML_CLASS_BASE}-variable-type',
            container
        )

    parameter_container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-parameters')],
        container
    )
    create_text_subelement(
        'h2',
        'Parameters',
        f'{HTML_CLASS_BASE}-function-header',
        parameter_container
    )
    for index, parameter in enumerate(signature.parameters.values()):

        var_container = create_subelement(
            'div',
            [('class', f'{HTML_CLASS_BASE}-function-parameters')],
            parameter_container
        )

        create_text_subelement(
            'var',
            parameter.name,
            f'{HTML_CLASS_BASE}-function-var',
            parameter_container
        )

        docstring_param = next(
            param
            for param in docstring.params
            if param.arg_name == parameter.name
        ) if docstring else None

        if parameter.annotation:
            type_name = _get_type_name(parameter.annotation, docstring_param)

            create_span_subelement(
                ': ',
                f'{HTML_CLASS_BASE}-punctuation',
                parameter_container
            )
            create_span_subelement(
                type_name,
                f'{HTML_CLASS_BASE}-variable-type',
                parameter_container
            )

        create_subelement('br', [], parameter_container)

        if docstring_param and docstring_param.description:
            create_text_subelement(
                'p',
                docstring_param.description,
                f'{HTML_CLASS_BASE}-function-param',
                parameter_container
            )

    return container


def _render_description(
        docstring: Optional[docstring_parser.Docstring],
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-description')],
        parent
    )

    if docstring and docstring.long_description:
        summary = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-function-description')],
            container
        )
        summary.text = docstring.long_description

    return container


def render_function(obj: Any, instructions: Set[str]) -> etree.Element:
    """Render a function

    <div class="function">
        <div class="function-title">
            <h1><span class="function-name">render_function</span> <span class="object-type">(function)</span><h1>
        </div>

        <div class="function-metadata">
            module: jetblack_markdown
            package: jetblack-markdown
            file: 
        <div>
    <div>

    :param obj: the function object
    :type obj: Any
    :param instructions: the render instructions
    :type instructions: Set[str]
    :return: The html etree
    :rtype: etree.Element
    """
    function_name = obj.__name__
    module_name = obj.__module__
    module = inspect.getmodule(obj)
    package_name = module.__package__ if module is not None else None
    file_name = module.__file__ if module is not None else None
    signature = inspect.signature(obj)
    docstring = docstring_parser.parse(inspect.getdoc(obj))

    container = etree.Element('div')
    container.set('class', f'{HTML_CLASS_BASE}-function')

    _render_function_title(obj, container)
    _render_meta_data(obj, container)
    _render_summary(docstring, container)
    _render_signature(obj, signature, docstring, container)
    _render_description(docstring, container)

    return container
