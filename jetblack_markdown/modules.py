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
    render_title_from_obj,
    render_summary,
    render_description,
    render_examples
)

def _render_module_meta_data(module: Any, parent: etree.Element) -> etree.Element:
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

def render_module_attributes(
        docstring: Docstring,
        md: Markdown,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-attributes')],
        parent
    )

    if docstring is None:
        return container
    attributes = [
        (meta.args[1], meta.description)
        for meta in docstring.meta
        if 'attribute' in meta.args
    ]
    if not attributes:
        return container

    create_text_subelement(
        'h3',
        'Attributes',
        f'{HTML_CLASS_BASE}-description',
        container
    )

    for attr_details, attr_desc in attributes:
        attr_container = create_subelement(
            'div',
            [('class', f'{HTML_CLASS_BASE}-class-attributes')],
            container
        )

        attr_name, sep, attr_type = attr_details.partition(' ')
        attr_type = attr_type.strip('()')

        create_text_subelement(
            'var',
            attr_name,
            f'{HTML_CLASS_BASE}-class-attr',
            attr_container
        )

        if attr_type:
            create_span_subelement(
                ': ',
                f'{HTML_CLASS_BASE}-punctuation',
                attr_container
            )
            create_span_subelement(
                attr_type,
                f'{HTML_CLASS_BASE}-variable-type',
                attr_container
            )

        create_subelement('br', [], attr_container)

        create_text_subelement(
            'p',
            md.convert(attr_desc),
            f'{HTML_CLASS_BASE}-class-attr',
            attr_container
        )

    return container

def render_module(
        obj: Any,
        md,
        parent: etree.Element
) -> etree.Element:
    docstring = docstring_parser.parse(inspect.getdoc(obj))

    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-module')],
        parent
    )

    render_title_from_obj(obj, container)
    _render_module_meta_data(obj, container)
    render_summary(docstring, container, md)
    render_module_attributes(docstring, md, container)
    render_description(docstring, container, md)
    render_examples(docstring, container, md)

    members = {
        name: value
        for name, value in  inspect.getmembers(obj)
    }

    return container

