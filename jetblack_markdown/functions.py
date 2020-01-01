"""Rendering functions
"""

import inspect
from inspect import Parameter
import typing
from typing import (
    Any,
    List,
    Optional,
    Set,
    Union
)

import docstring_parser
from docstring_parser import (
    Docstring,
    DocstringParam,
    DocstringReturns
)
from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .utils import (
    create_subelement,
    create_span_subelement,
    create_text_subelement,
    find_docstring_param,
    get_type_name
)


def _render_function_title(obj: Any, parent: etree.Element) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-title')],
        parent
    )

    header = create_subelement(
        'h2',
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
        docstring: Optional[Docstring],
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-summary')],
        parent
    )

    if docstring and docstring.short_description:
        create_text_subelement(
            'h3',
            'Summary',
            f'{HTML_CLASS_BASE}-function-summary',
            container
        )
        summary = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-function-summary')],
            container
        )
        summary.text = docstring.short_description

    return container


def _render_signature(
        obj: Any,
        signature: inspect.Signature,
        docstring: Docstring,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'code',
        [('class', f'{HTML_CLASS_BASE}-function-signature')],
        parent
    )

    create_span_subelement(
        obj.__name__,
        f'{HTML_CLASS_BASE}-function-name',
        container
    )

    create_span_subelement('(', f'{HTML_CLASS_BASE}-punctuation', container)

    is_pos_only_rendered = False
    is_kw_only_rendered = False

    for index, parameter in enumerate(signature.parameters.values()):
        if index:
            create_span_subelement(
                ', ',
                f'{HTML_CLASS_BASE}-punctuation',
                container
            )

        if parameter.kind is Parameter.VAR_POSITIONAL:
            arg_name = '*' + parameter.name
            type_name = None
        elif parameter.kind is Parameter.VAR_KEYWORD:
            arg_name = '**' + parameter.name
            type_name = None
        else:
            if parameter.kind is Parameter.POSITIONAL_ONLY and not is_pos_only_rendered:
                create_text_subelement(
                    'var',
                    '/',
                    f'{HTML_CLASS_BASE}-function-var',
                    container
                )
                create_span_subelement(
                    ', ',
                    f'{HTML_CLASS_BASE}-punctuation',
                    container
                )
                is_pos_only_rendered = True
            elif parameter.kind is Parameter.KEYWORD_ONLY and not is_kw_only_rendered:
                create_text_subelement(
                    'var',
                    '*',
                    f'{HTML_CLASS_BASE}-function-var',
                    container
                )
                create_span_subelement(
                    ', ',
                    f'{HTML_CLASS_BASE}-punctuation',
                    container
                )
                is_kw_only_rendered = True

            arg_name = parameter.name

            docstring_param = find_docstring_param(
                parameter.name,
                docstring
            )

            type_name = get_type_name(parameter.annotation, docstring_param)

        create_text_subelement(
            'var',
            arg_name,
            f'{HTML_CLASS_BASE}-function-var',
            container
        )

        if type_name:
            create_span_subelement(
                ': ', f'{HTML_CLASS_BASE}-punctuation', container)
            create_span_subelement(
                type_name,
                f'{HTML_CLASS_BASE}-variable-type',
                container
            )

    create_span_subelement(')', f'{HTML_CLASS_BASE}-punctuation', container)

    if signature.return_annotation:
        type_name = get_type_name(
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


def _render_parameters(
        obj: Any,
        signature: inspect.Signature,
        docstring: Docstring,
        parent: etree.Element
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
    for index, parameter in enumerate(signature.parameters.values()):

        parameter_container = create_subelement(
            'div',
            [('class', f'{HTML_CLASS_BASE}-function-parameters')],
            container
        )

        docstring_param = find_docstring_param(
            parameter.name,
            docstring
        )

        if parameter.kind is Parameter.VAR_POSITIONAL:
            arg_name = '*' + parameter.name
            type_name = None
        elif parameter.kind is Parameter.VAR_KEYWORD:
            arg_name = '**' + parameter.name
            type_name = None
        else:
            arg_name = parameter.name
            type_name = get_type_name(parameter.annotation, docstring_param)

        create_text_subelement(
            'var',
            arg_name,
            f'{HTML_CLASS_BASE}-function-var',
            parameter_container
        )

        if type_name:
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

        description = docstring_param.description if docstring_param else ''
        create_text_subelement(
            'p',
            description,
            f'{HTML_CLASS_BASE}-function-param',
            parameter_container
        )

    return container


def _render_returns(
        obj: Any,
        signature: inspect.Signature,
        docstring: Docstring,
        parent: etree.Element
) -> etree.Element:

    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-function-returns')],
        parent
    )
    create_text_subelement(
        'h3',
        'Returns',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    type_name = get_type_name(signature.return_annotation, docstring.returns)

    create_span_subelement(
        type_name,
        f'{HTML_CLASS_BASE}-variable-type',
        container
    )
    create_span_subelement(
        ': ',
        f'{HTML_CLASS_BASE}-punctuation',
        container
    )

    description = docstring.returns.description if docstring.returns else ''
    create_span_subelement(
        description,
        f'{HTML_CLASS_BASE}-function-param',
        container
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
        create_text_subelement(
            'h3',
            'Description',
            f'{HTML_CLASS_BASE}-function-description',
            container
        )
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
    signature = inspect.signature(obj)
    docstring = docstring_parser.parse(inspect.getdoc(obj))

    container = etree.Element('div')
    container.set('class', f'{HTML_CLASS_BASE}-function')

    _render_function_title(obj, container)
    _render_meta_data(obj, container)
    _render_summary(docstring, container)
    _render_signature(obj, signature, docstring, container)
    _render_parameters(obj, signature, docstring, container)
    _render_returns(obj, signature, docstring, container)
    _render_description(docstring, container)

    return container
