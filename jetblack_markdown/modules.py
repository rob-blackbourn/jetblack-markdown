"""Module rendering"""

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
from .renderers import (
    render_title,
    render_summary,
    render_description,
    render_examples
)

def _render_meta_data(module: Any, parent: etree.Element) -> etree.Element:
    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-metadata')],
        parent
    )

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

def render_module(obj: Any, instructions: Set[str], md) -> etree.Element:
    docstring = docstring_parser.parse(inspect.getdoc(obj))

    container = etree.Element('div')
    container.set('class', f'{HTML_CLASS_BASE}-module')

    render_title(obj, container)
    _render_meta_data(obj, container)
    render_summary(docstring, container, md)
    render_description(docstring, container, md)
    render_examples(docstring, container, md)

    return container

