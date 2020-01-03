"""Module rendering"""

import inspect
from inspect import Parameter
import typing
from typing import (
    Any,
    Dict,
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
    render_title_from_obj,
    render_summary,
    render_description,
    render_examples
)
from .functions import (
    _render_meta_data,
    _render_signature,
    _render_parameters,
    _render_yields,
    _render_returns,
    _render_raises,
    create_function
)

def render_property(
        obj: Any,
        klass: Any,
        property_name: str,
        instructions: Set[str],
        md: Markdown,
        class_from_init: bool,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-raises')],
        parent
    )

    render_title(f'{klass.__name__}.{property_name}', "property", container)
    _render_meta_data(klass, container)

    signature = inspect.signature(obj.fget)
    docstring = docstring_parser.parse(inspect.getdoc(obj))
    render_summary(docstring, container, md)

    members = {
        name: value
        for name, value in inspect.getmembers(obj)
    }

    code = create_subelement(
        'code',
        [('class', f'{HTML_CLASS_BASE}-function-signature')],
        container
    )

    create_span_subelement(
        f'{klass.__name__}.{property_name}',
        f'{HTML_CLASS_BASE}-type',
        code
    )
    create_span_subelement(
        ': ',
        f'{HTML_CLASS_BASE}-punctuation',
        code
    )
    type_name = get_type_name(signature.return_annotation, docstring.returns)
    create_span_subelement(
        type_name,
        f'{HTML_CLASS_BASE}-type',
        code
    )
    create_span_subelement(
        ' = ...\n',
        f'{HTML_CLASS_BASE}-punctuation',
        code
    )
    # create_subelement('br', [], code)

    if members['fset']:
        code = create_subelement(
            'code',
            [('class', f'{HTML_CLASS_BASE}-function-signature')],
            container
        )
        create_span_subelement(
            f'{klass.__name__}.{property_name}',
            f'{HTML_CLASS_BASE}-type',
            code
        )
        create_span_subelement(
            ' -> ',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        type_name = get_type_name(signature.return_annotation, docstring.returns)
        create_span_subelement(
            type_name,
            f'{HTML_CLASS_BASE}-type',
            code
        )
        create_span_subelement(
            '\n',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        # create_subelement('br', [], code)

    if members['fdel']:
        code = create_subelement(
            'code',
            [('class', f'{HTML_CLASS_BASE}-function-signature')],
            container
        )
        create_span_subelement(
            'del ',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        create_span_subelement(
            f'{klass.__name__}.{property_name}',
            f'{HTML_CLASS_BASE}-type',
            code
        )
        create_span_subelement(
            '\n',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        # create_subelement('br', [], code)

    _render_raises(obj, signature, docstring, container, md)
    render_description(docstring, container, md)
    render_examples(docstring, container, md)

    return container

def render_class(
        obj: Any,
        instructions: Set[str],
        md: Markdown,
        class_from_init: bool,
        ignore_dunder: bool,
        ignore_private: bool
) -> etree.Element:
    members: Dict[str, Any] = {
        name: value
        for name, value in inspect.getmembers(obj)
    }
    signature = inspect.signature(obj)
    docstring = docstring_parser.parse(
        inspect.getdoc(
            members['__init__'] if class_from_init else obj
        )
    )

    container = etree.Element('div')
    container.set('class', f'{HTML_CLASS_BASE}-class')

    render_title_from_obj(obj, container)
    _render_meta_data(obj, container)
    render_summary(docstring, container, md)
    _render_signature(obj, signature, docstring, container, 'constructor')
    _render_parameters(obj, signature, docstring, container, md, 'constructor')
    _render_raises(obj, signature, docstring, container, md)
    render_description(docstring, container, md)
    render_examples(docstring, container, md)

    for name, member in members.items():
        if name == '__init__' or (
                ignore_dunder and
                name.startswith('__') and
                name.endswith('__')
        ) or (ignore_private and name.startswith('_')):
            continue

        para = create_subelement(
            'div',
            [('class', f'{HTML_CLASS_BASE}-function')],
            container
        )
        if member.__class__ is property:
            render_property(
                member,
                obj,
                name,
                instructions,
                md,
                class_from_init,
                para
            )
        elif inspect.isfunction(member):
            create_function(member, instructions, md, para, 'method')

    return container

