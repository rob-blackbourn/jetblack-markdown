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


def render_title(obj: Any, parent: etree.Element) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-title')],
        parent
    )

    header = create_subelement(
        'h2',
        [('class', f'{HTML_CLASS_BASE}-header')],
        container
    )

    create_span_subelement(
        obj.__name__,
        f'{HTML_CLASS_BASE}-name',
        header
    )
    create_span_subelement(
        ' ',
        None,
        header
    )

    if inspect.ismodule(obj):
        create_span_subelement(
            '(module)',
            f'{HTML_CLASS_BASE}-object-type',
            header
        )
    elif inspect.isgeneratorfunction(obj):
        create_span_subelement(
            '(generator function)',
            f'{HTML_CLASS_BASE}-object-type',
            header
        )
    elif inspect.isasyncgenfunction(obj):
        create_span_subelement(
            '(async generator function)',
            f'{HTML_CLASS_BASE}-object-type',
            header
        )
    else:
        create_span_subelement(
            '(function)',
            f'{HTML_CLASS_BASE}-object-type',
            header
        )

    return container



def render_summary(
        docstring: Optional[Docstring],
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-summary')],
        parent
    )

    if docstring and docstring.short_description:
        create_text_subelement(
            'h3',
            'Summary',
            f'{HTML_CLASS_BASE}-summary',
            container
        )
        summary = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-function-summary')],
            container
        )
        summary.text = docstring.short_description

    return container


def render_description(
        docstring: Optional[docstring_parser.Docstring],
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-description')],
        parent
    )

    if docstring and docstring.long_description:
        create_text_subelement(
            'h3',
            'Description',
            f'{HTML_CLASS_BASE}-description',
            container
        )
        summary = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-description')],
            container
        )
        summary.text = docstring.long_description

    return container
