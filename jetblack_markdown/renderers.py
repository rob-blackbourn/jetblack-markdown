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



def render_title(name: str, object_type: str, parent: etree.Element) -> etree.Element:
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
        name.replace('_', '&lowbar;'),
        f'{HTML_CLASS_BASE}-name',
        header
    )
    create_span_subelement(
        ' ',
        None,
        header
    )

    create_span_subelement(
        f'({object_type})',
        f'{HTML_CLASS_BASE}-object-type',
        header
    )

    return container


def render_title_from_obj(obj: Any, parent: etree.Element) -> etree.Element:
    name = obj.__qualname__ if hasattr(obj, '__qualname__') else obj.__name__
    if inspect.ismodule(obj):
        object_type = 'module'
    elif inspect.isclass(obj):
        object_type = 'class'
    elif inspect.isgeneratorfunction(obj):
        object_type = 'generator function'
    elif inspect.isasyncgenfunction(obj):
        object_type = 'async generator function'
    else:
        object_type = 'function'

    return render_title(name, object_type, parent)



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

def render_meta_data(
        module_name: Optional[str],
        package_name: Optional[str],
        file_name: Optional[str],
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-metadata')],
        parent
    )

    if module_name:
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
            module_name,
            f'{HTML_CLASS_BASE}-metadata-value',
            container
        )
        create_subelement('br', [], container)

    if package_name:
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
            package_name,
            f'{HTML_CLASS_BASE}-metadata-value',
            container
        )
        create_subelement('br', [], container)

    if file_name:
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
            file_name,
            f'{HTML_CLASS_BASE}-metadata-value',
            container
        )
        create_subelement('br', [], container)

    return container
