"""Rendering functions
"""

import inspect
from inspect import Parameter
from typing import (
    Any,
    List,
    Optional,
    Tuple
)

import docstring_parser
from docstring_parser import (
    Docstring
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
    render_summary_obj,
    render_description_obj,
    render_examples_obj,
    render_meta_data
)




def _render_meta_data_obj(obj: Any, parent: etree.Element) -> etree.Element:
    module = inspect.getmodule(obj)
    return render_meta_data(
        obj.__module__,
        module.__package__ if module else None,
        module.__file__ if module else None,
        parent
    )

def _render_signature(
        name: str,
        is_async: bool,
        parameters: List[Tuple[str, Optional[str]]],
        return_type_name: Optional[str],
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'code',
        [('class', f'{HTML_CLASS_BASE}-function-signature')],
        parent
    )

    if is_async:
        create_span_subelement(
            "async ",
            f'{HTML_CLASS_BASE}-function-punctuation',
            container
        )

    create_span_subelement(
        name,
        f'{HTML_CLASS_BASE}-function-name',
        container
    )

    create_span_subelement('(', f'{HTML_CLASS_BASE}-punctuation', container)

    is_first = True
    for arg_name, type_name in parameters:
        if is_first:
            is_first = False
        else:
            create_span_subelement(
                ', ',
                f'{HTML_CLASS_BASE}-punctuation',
                container
            )

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

    if return_type_name:
        create_span_subelement(
            ' -> ', f'{HTML_CLASS_BASE}-punctuation', container)
        create_span_subelement(
            return_type_name,
            f'{HTML_CLASS_BASE}-variable-type',
            container
        )

def _render_signature_obj(
        obj: Any,
        signature: inspect.Signature,
        docstring: Docstring,
        parent: etree.Element,
        function_type: str
) -> etree.Element:

    is_async = inspect.iscoroutinefunction(obj) or inspect.isasyncgenfunction(obj)
    name = obj.__qualname__ if hasattr(obj, '__qualname__') else obj.__name__

    parameters: List[Tuple[str, Optional[str]]] = []
    is_pos_only_rendered = False
    is_kw_only_rendered = False
    is_self = function_type in {'method', 'constructor'}
    for parameter in signature.parameters.values():
        if is_self:
            is_self = False
            continue

        if parameter.kind is Parameter.VAR_POSITIONAL:
            arg_name = '*' + parameter.name
            type_name = None
        elif parameter.kind is Parameter.VAR_KEYWORD:
            arg_name = '**' + parameter.name
            type_name = None
        else:
            if parameter.kind is Parameter.POSITIONAL_ONLY and not is_pos_only_rendered:
                parameters.append(('/', None))
                is_pos_only_rendered = True
            elif parameter.kind is Parameter.KEYWORD_ONLY and not is_kw_only_rendered:
                parameters.append(('*', None))
                is_kw_only_rendered = True

            arg_name = parameter.name

            docstring_param = find_docstring_param(
                parameter.name,
                docstring
            )

            type_name = get_type_name(parameter.annotation, docstring_param)

        parameters.append((arg_name, type_name))

    return_type_name: Optional[str] = None
    if signature.return_annotation and function_type != 'constructor':
        return_type_name = get_type_name(
            signature.return_annotation,
            docstring.returns if docstring else None
        )

    return _render_signature(name, is_async, parameters, return_type_name, parent)    


def _render_parameters(
        obj: Any,
        signature: inspect.Signature,
        docstring: Docstring,
        parent: etree.Element,
        md: Markdown,
        function_type: str
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

    is_self = function_type in {'method', 'constructor'}
    for parameter in signature.parameters.values():
        if is_self:
            is_self = False
            continue

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

        if parameter.default != Parameter.empty:
            create_span_subelement(
                ' (optional)',
                f'{HTML_CLASS_BASE}-punctuation',
                parameter_container
            )


        create_subelement('br', [], parameter_container)

        description = docstring_param.description if docstring_param else ''
        create_text_subelement(
            'p',
            md.convert(description),
            f'{HTML_CLASS_BASE}-function-param',
            parameter_container
        )

    return container


def _render_returns(
        obj: Any,
        signature: inspect.Signature,
        docstring: Docstring,
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-function-returns')],
        parent
    )

    type_name = get_type_name(signature.return_annotation, docstring.returns)
    if type_name == 'None' or type_name == 'typing.None':
        return container

    create_text_subelement(
        'h3',
        'Returns',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

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
    text = md.convert(description)
    if text.startswith('<p>') and text.endswith('</p>'):
        text = text[3:-4]
    create_span_subelement(
        text,
        f'{HTML_CLASS_BASE}-description',
        container
    )

    return container

def _render_yields(
        obj: Any,
        signature: inspect.Signature,
        docstring: Docstring,
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-function-yields')],
        parent
    )

    type_name = get_type_name(signature.return_annotation, docstring.returns)
    if type_name == 'None' or type_name == 'typing.None':
        return container

    create_text_subelement(
        'h3',
        'Yields',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

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
    text = md.convert(description)
    if text.startswith('<p>') and text.endswith('</p>'):
        text = text[3:-4]
    create_span_subelement(
        text,
        f'{HTML_CLASS_BASE}-description',
        container
    )

    return container


def _render_raises(
        obj: Any,
        signature: inspect.Signature,
        docstring: Docstring,
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-raises')],
        parent
    )
    if not docstring.raises:
        return container

    create_text_subelement(
        'h3',
        'Raises',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    for error in docstring.raises:
        error_container = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-function-raises')],
            container
        )

        create_span_subelement(
            error.type_name,
            f'{HTML_CLASS_BASE}-variable-type',
            error_container
        )
        create_span_subelement(
            ': ',
            f'{HTML_CLASS_BASE}-punctuation',
            error_container
        )

        text = md.convert(error.description)
        if text.startswith('<p>') and text.endswith('</p>'):
            text = text[3:-4]
        create_span_subelement(
            text,
            f'{HTML_CLASS_BASE}-function-raises',
            error_container
        )

    return container


    
def create_function(
        obj: Any,
        md: Markdown,
        container: etree.Element,
        function_type: str
) -> etree.Element:
    signature = inspect.signature(obj)
    docstring = docstring_parser.parse(inspect.getdoc(obj))

    render_title_from_obj(obj, container)
    _render_meta_data_obj(obj, container)
    render_summary_obj(docstring, container, md)
    _render_signature_obj(obj, signature, docstring, container, function_type)
    _render_parameters(obj, signature, docstring, container, md, function_type)

    if inspect.isgeneratorfunction(obj) or inspect.isasyncgenfunction(obj):
        _render_yields(obj, signature, docstring, container, md)
    else:
        _render_returns(obj, signature, docstring, container, md)
    _render_raises(obj, signature, docstring, container, md)
    render_description_obj(docstring, container, md)
    render_examples_obj(docstring, container, md)

    return container

def render_function(
        obj: Any,
        md: Markdown,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-function')],
        parent
    )
    return create_function(obj, md, container, 'function')

