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
from markdown import Markdown
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
        parent: etree.Element,
        md: Markdown
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
        summary.text = md.convert(docstring.short_description)

    return container


def render_description(
        docstring: Optional[docstring_parser.Docstring],
        parent: etree.Element,
        md: Markdown
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
        description = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-description')],
            container
        )
        description.text = md.convert(docstring.long_description)

    return container

def render_examples(
        docstring: Optional[docstring_parser.Docstring],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-examples')],
        parent
    )

    if docstring is None:
        return container
    examples = [
        meta.description
        for meta in docstring.meta
        if 'examples' in meta.args
    ]
    if not examples:
        return container

    create_text_subelement(
        'h3',
        'Examples',
        f'{HTML_CLASS_BASE}-description',
        container
    )

    for example in examples:
        paragraph = create_subelement('p', [], container)
        paragraph.text = md.convert(example)

    return container