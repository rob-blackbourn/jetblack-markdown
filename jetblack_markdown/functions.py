"""Rendering functions
"""

import inspect
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


def _render_signature(obj: Any, parent: etree.Element) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-signature')],
        parent
    )


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

    parameters: List[str] = []
    for param in signature.parameters.values():
        parameter = param.name
        if param.annotation:
            parameter += f': {param.annotation.__name__}'
        parameters.append(parameter)

    prototype = etree.SubElement(container, 'p')
    prototype.text = f'{function_name}({", ".join(parameters)})'

    return container
