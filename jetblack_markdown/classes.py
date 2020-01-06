"""Module rendering"""

import inspect
from typing import (
    Any,
    Dict,
    Set
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
    render_summary_obj,
    render_description_obj,
    render_examples_obj
)
from .functions import (
    _render_meta_data_obj,
    _render_signature_obj,
    _render_parameters,
    _render_raises,
    create_function
)

def render_property(
        obj: Any,
        klass: Any,
        property_name: str,
        md: Markdown,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-raises')],
        parent
    )

    render_title(f'{klass.__name__}.{property_name}', "property", container)
    _render_meta_data_obj(klass, container)

    signature = inspect.signature(obj.fget)
    docstring = docstring_parser.parse(inspect.getdoc(obj))
    render_summary_obj(docstring, container, md)

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
    render_description_obj(docstring, container, md)
    render_examples_obj(docstring, container, md)

    return container

def render_class_attributes(
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

def render_class(
        obj: Any,
        md: Markdown,
        class_from_init: bool,
        ignore_dunder: bool,
        ignore_private: bool,
        parent: etree.Element
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

    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-class')],
        parent
    )

    render_title_from_obj(obj, container)
    _render_meta_data_obj(obj, container)
    render_summary_obj(docstring, container, md)
    _render_signature_obj(obj, signature, docstring, container, 'constructor')
    _render_parameters(obj, signature, docstring, container, md, 'constructor')
    render_class_attributes(docstring, md, container)
    _render_raises(obj, signature, docstring, container, md)
    render_description_obj(docstring, container, md)
    render_examples_obj(docstring, container, md)

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
                md,
                para
            )
        elif inspect.isfunction(member):
            create_function(member, md, para, 'method')

    return container

