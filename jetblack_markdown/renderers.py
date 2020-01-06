"""Rendering functions
"""

from typing import (
    List,
    Optional
)

from markdown import Markdown
from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .utils import (
    add_tag,
    add_span_tag,
    add_text_tag
)

from .metadata import (
    ArgumentDescriptor,
    PropertyDescriptor,
    RaisesDescriptor,
    FunctionDescriptor,
    ClassDescriptor,
    ModuleDescriptor
)

def render_title(name: str, object_type: str, parent: etree.Element) -> etree.Element:
    container = add_tag('div', f'{HTML_CLASS_BASE}-title',parent)
    header = add_tag('h2', f'{HTML_CLASS_BASE}-header', container)
    add_span_tag(name.replace('_', '&lowbar;'), f'{HTML_CLASS_BASE}-name', header)
    add_span_tag(' ', None, header)

    add_span_tag(
        f'({object_type})',
        f'{HTML_CLASS_BASE}-object-type',
        header
    )

    return container


def render_summary(
        summary: Optional[str],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:
    container = add_tag('div', f'{HTML_CLASS_BASE}-summary', parent)

    if summary:
        add_text_tag('h3', 'Summary', f'{HTML_CLASS_BASE}-summary', container)
        paragraph = add_tag('p', f'{HTML_CLASS_BASE}-function-summary', container)
        paragraph.text = md.convert(summary)

    return container


def render_description(
        description: Optional[str],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:
    container = add_tag('div', f'{HTML_CLASS_BASE}-description', parent)

    if description:
        add_text_tag('h3', 'Description', f'{HTML_CLASS_BASE}-description', container)
        paragraph = add_tag('p', f'{HTML_CLASS_BASE}-description', container)
        paragraph.text = md.convert(description)


def render_examples(
        examples: Optional[List[str]],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:
    container = add_tag('div', f'{HTML_CLASS_BASE}-examples', parent)

    if not examples:
        return container

    add_text_tag('h3', 'Examples', f'{HTML_CLASS_BASE}-description', container)

    for example in examples:
        paragraph = add_tag('p', None, container)
        paragraph.text = md.convert(example)

    return container

def render_meta_data(
        module_name: Optional[str],
        package_name: Optional[str],
        file_name: Optional[str],
        parent: etree.Element
) -> etree.Element:
    container = add_tag('p', f'{HTML_CLASS_BASE}-metadata', parent)

    if module_name:
        add_text_tag(
            'strong',
            'Module:',
            f'{HTML_CLASS_BASE}-metadata-header',
            container
        )
        add_span_tag(
            ' ',
            None,
            container
        )
        add_span_tag(
            module_name,
            f'{HTML_CLASS_BASE}-metadata-value',
            container
        )
        add_tag('br', None, container)

    if package_name:
        add_text_tag(
            'strong',
            'Package: ',
            f'{HTML_CLASS_BASE}-metadata-header',
            container
        )
        add_span_tag(
            ' ',
            None,
            container
        )
        add_span_tag(
            package_name,
            f'{HTML_CLASS_BASE}-metadata-value',
            container
        )
        add_tag('br', None, container)

    if file_name:
        add_text_tag(
            'strong',
            'File',
            f'{HTML_CLASS_BASE}-metadata-header',
            container
        )
        add_span_tag(
            ': ',
            None,
            container
        )
        add_span_tag(
            file_name,
            f'{HTML_CLASS_BASE}-metadata-value',
            container
        )
        add_tag('br', None, container)

    return container


def render_attributes(
        attributes: List[ArgumentDescriptor],
        md: Markdown,
        parent: etree.Element
) -> etree.Element:
    container = add_tag('div', f'{HTML_CLASS_BASE}-attributes',parent)

    if not attributes:
        return container

    add_text_tag(
        'h3',
        'Attributes',
        f'{HTML_CLASS_BASE}-description',
        container
    )

    for attribute in attributes:
        attr_container = add_tag('div', f'{HTML_CLASS_BASE}-attributes', container)

        add_text_tag(
            'var',
            attribute.name,
            f'{HTML_CLASS_BASE}-name',
            attr_container
        )

        if attribute.type:
            add_span_tag(
                ': ',
                f'{HTML_CLASS_BASE}-punctuation',
                attr_container
            )
            add_span_tag(
                attribute.type,
                f'{HTML_CLASS_BASE}-vartype',
                attr_container
            )

        add_tag('br', None, attr_container)

        add_text_tag(
            'p',
            md.convert(attribute.description or ''),
            f'{HTML_CLASS_BASE}-description',
            attr_container
        )

    return container
    
def render_property(
        property_descriptor: PropertyDescriptor,
        md: Markdown,
        parent: etree.Element
) -> etree.Element:
    container = add_tag('div', f'{HTML_CLASS_BASE}-function-raises',parent)

    render_title(property_descriptor.qual_name, "property", container)
    # _render_meta_data_obj(klass, container)

    render_summary(property_descriptor.summary, container, md)

    code = add_tag('code', f'{HTML_CLASS_BASE}-function-signature', container)

    add_span_tag(
        property_descriptor.qual_name,
        f'{HTML_CLASS_BASE}-type',
        code
    )
    add_span_tag(
        ': ',
        f'{HTML_CLASS_BASE}-punctuation',
        code
    )
    add_span_tag(
        property_descriptor.type or 'Any',
        f'{HTML_CLASS_BASE}-type',
        code
    )
    add_span_tag(
        ' = ...\n',
        f'{HTML_CLASS_BASE}-punctuation',
        code
    )

    if property_descriptor.is_settable:
        code = add_tag('code', f'{HTML_CLASS_BASE}-function-signature', container)
        add_span_tag(
            property_descriptor.qual_name,
            f'{HTML_CLASS_BASE}-type',
            code
        )
        add_span_tag(
            ' -> ',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        add_span_tag(
            property_descriptor.type or 'Any',
            f'{HTML_CLASS_BASE}-type',
            code
        )
        add_span_tag(
            '\n',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )

    if property_descriptor.is_deletable:
        code = add_tag('code', f'{HTML_CLASS_BASE}-function-signature', container)
        add_span_tag(
            'del ',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        add_span_tag(
            property_descriptor.qual_name,
            f'{HTML_CLASS_BASE}-type',
            code
        )
        add_span_tag(
            '\n',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )

    render_raises(property_descriptor.raises, container, md)
    render_description(property_descriptor.description, container, md)
    render_examples(property_descriptor.examples, container, md)

    return container

def render_class(
        class_descriptor: ClassDescriptor,
        md: Markdown,
        parent: etree.Element
) -> etree.Element:

    container = add_tag('div', f'{HTML_CLASS_BASE}-class', parent)

    render_title(class_descriptor.name, 'class', container)
    render_meta_data(class_descriptor.module, class_descriptor.package, class_descriptor.file, container)
    render_summary(class_descriptor.summary, container, md)
    render_signature(class_descriptor.constructor, container)
    render_parameters(class_descriptor.constructor.arguments, container, md)
    render_attributes(class_descriptor.attributes, md, container)
    render_raises(class_descriptor.constructor.raises, container, md)
    render_description(class_descriptor.description, container, md)
    render_examples(class_descriptor.examples, container, md)
    for prop in class_descriptor.properties:
        render_property(prop, md, container)
    for method in class_descriptor.methods:
        render_function_in_container(method, md, container)

    return container

def render_signature(
        function_descriptor: FunctionDescriptor,
        parent: etree.Element
) -> etree.Element:
    container = add_tag('code', f'{HTML_CLASS_BASE}-function-signature', parent)

    if function_descriptor.is_async:
        add_span_tag(
            "async ",
            f'{HTML_CLASS_BASE}-function-punctuation',
            container
        )

    add_span_tag(
        function_descriptor.name,
        f'{HTML_CLASS_BASE}-function-name',
        container
    )

    add_span_tag('(', f'{HTML_CLASS_BASE}-punctuation', container)

    is_first = True
    for argument in function_descriptor.arguments:
        if is_first:
            is_first = False
        else:
            add_span_tag(
                ', ',
                f'{HTML_CLASS_BASE}-punctuation',
                container
            )

        add_text_tag(
            'var',
            argument.name,
            f'{HTML_CLASS_BASE}-function-var',
            container
        )

        if argument.type:
            add_span_tag(
                ': ', f'{HTML_CLASS_BASE}-punctuation', container)
            add_span_tag(
                argument.type,
                f'{HTML_CLASS_BASE}-variable-type',
                container
            )

    add_span_tag(')', f'{HTML_CLASS_BASE}-punctuation', container)

    if function_descriptor.return_type:
        add_span_tag(
            ' -> ', f'{HTML_CLASS_BASE}-punctuation', container)
        add_span_tag(
            function_descriptor.return_type,
            f'{HTML_CLASS_BASE}-variable-type',
            container
        )


def render_parameters(
        arguments: List[ArgumentDescriptor],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = add_tag('div', f'{HTML_CLASS_BASE}-function-parameters', parent)
    add_text_tag(
        'h3',
        'Parameters',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    for argument in arguments:

        parameter_container = add_tag('div', f'{HTML_CLASS_BASE}-function-parameters', container)

        add_text_tag(
            'var',
            argument.name,
            f'{HTML_CLASS_BASE}-function-var',
            parameter_container
        )

        if argument.type:
            add_span_tag(': ', f'{HTML_CLASS_BASE}-punctuation', parameter_container)
            add_span_tag(argument.type, f'{HTML_CLASS_BASE}-vartype', parameter_container)

        if argument.is_optional:
            add_span_tag(' (optional)', f'{HTML_CLASS_BASE}-punctuation', parameter_container)


        add_tag('br', None, parameter_container)

        add_text_tag('p', md.convert(argument.description or ''), f'{HTML_CLASS_BASE}-function-param', parameter_container)

    return container


def render_returns(
        function_descriptor: FunctionDescriptor,
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = add_tag('p', f'{HTML_CLASS_BASE}-function-returns', parent)

    if not function_descriptor.return_type or function_descriptor.return_type in ('None', 'typing.None'):
        return container

    add_text_tag(
        'h3',
        'Yields' if function_descriptor.is_generator else 'Returns',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    add_span_tag(
        function_descriptor.return_type,
        f'{HTML_CLASS_BASE}-variable-type',
        container
    )
    add_span_tag(
        ': ',
        f'{HTML_CLASS_BASE}-punctuation',
        container
    )

    description = function_descriptor.return_description or ''
    text = md.convert(description)
    if text.startswith('<p>') and text.endswith('</p>'):
        text = text[3:-4]
    add_span_tag(
        text,
        f'{HTML_CLASS_BASE}-description',
        container
    )

    return container


def render_raises(
        raises: Optional[List[RaisesDescriptor]],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = add_tag('div', f'{HTML_CLASS_BASE}-function-raises', parent)
    if not raises:
        return container

    add_text_tag(
        'h3',
        'Raises',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    for error in raises:
        error_container = add_tag('p', f'{HTML_CLASS_BASE}-function-raises', container)

        add_span_tag(
            error.type,
            f'{HTML_CLASS_BASE}-variable-type',
            error_container
        )
        add_span_tag(
            ': ',
            f'{HTML_CLASS_BASE}-punctuation',
            error_container
        )

        text = md.convert(error.description)
        if text.startswith('<p>') and text.endswith('</p>'):
            text = text[3:-4]
        add_span_tag(
            text,
            f'{HTML_CLASS_BASE}-function-raises',
            error_container
        )

    return container


def render_function_in_container(
        function_descriptor: FunctionDescriptor,
        md: Markdown,
        container: etree.Element
) -> etree.Element:

    render_title(function_descriptor.name, function_descriptor.function_type_name, container)
    render_meta_data(function_descriptor.module, function_descriptor.package, function_descriptor.file, container)
    render_summary(function_descriptor.summary, container, md)
    render_signature(function_descriptor, container)
    render_parameters(function_descriptor.arguments, container, md)
    render_returns(function_descriptor, container, md)
    render_raises(function_descriptor.raises, container, md)
    render_description(function_descriptor.description, container, md)
    render_examples(function_descriptor.examples, container, md)

    return container

def render_function(
        function_descriptor: FunctionDescriptor,
        md: Markdown,
        parent: etree.Element
) -> etree.Element:
    container = add_tag('p', f'{HTML_CLASS_BASE}-function', parent)

    return render_function_in_container(function_descriptor, md, container)


def render_module(
        module_descriptor: ModuleDescriptor,
        md,
        parent: etree.Element
) -> etree.Element:
    container = add_tag('div', f'{HTML_CLASS_BASE}-module', parent)

    render_title(module_descriptor.name, 'module', container)
    render_meta_data(None, module_descriptor.package, module_descriptor.file, container)
    render_summary(module_descriptor.summary, container, md)
    render_attributes(module_descriptor.attributes, md, container)
    render_description(module_descriptor.description, container, md)
    render_examples(module_descriptor.examples, container, md)

    return container
