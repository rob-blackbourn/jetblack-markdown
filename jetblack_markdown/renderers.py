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
    create_subelement,
    create_span_subelement,
    create_text_subelement
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


def render_summary(
        summary: Optional[str],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-summary')],
        parent
    )

    if summary:
        create_text_subelement(
            'h3',
            'Summary',
            f'{HTML_CLASS_BASE}-summary',
            container
        )
        paragraph = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-function-summary')],
            container
        )
        paragraph.text = md.convert(summary)

    return container


def render_description(
        description: Optional[str],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-description')],
        parent
    )

    if description:
        create_text_subelement(
            'h3',
            'Description',
            f'{HTML_CLASS_BASE}-description',
            container
        )
        paragraph = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-description')],
            container
        )
        paragraph.text = md.convert(description)


def render_examples(
        examples: Optional[List[str]],
        parent: etree.Element,
        md: Markdown
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-examples')],
        parent
    )

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


def render_attributes(
        attributes: List[ArgumentDescriptor],
        md: Markdown,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-attributes')],
        parent
    )

    if not attributes:
        return container

    create_text_subelement(
        'h3',
        'Attributes',
        f'{HTML_CLASS_BASE}-description',
        container
    )

    for attribute in attributes:
        attr_container = create_subelement(
            'div',
            [('class', f'{HTML_CLASS_BASE}-attributes')],
            container
        )

        create_text_subelement(
            'var',
            attribute.name,
            f'{HTML_CLASS_BASE}-name',
            attr_container
        )

        if attribute.type:
            create_span_subelement(
                ': ',
                f'{HTML_CLASS_BASE}-punctuation',
                attr_container
            )
            create_span_subelement(
                attribute.type,
                f'{HTML_CLASS_BASE}-vartype',
                attr_container
            )

        create_subelement('br', [], attr_container)

        create_text_subelement(
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
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-raises')],
        parent
    )

    render_title(property_descriptor.qual_name, "property", container)
    # _render_meta_data_obj(klass, container)

    render_summary(property_descriptor.summary, container, md)

    code = create_subelement(
        'code',
        [('class', f'{HTML_CLASS_BASE}-function-signature')],
        container
    )

    create_span_subelement(
        property_descriptor.qual_name,
        f'{HTML_CLASS_BASE}-type',
        code
    )
    create_span_subelement(
        ': ',
        f'{HTML_CLASS_BASE}-punctuation',
        code
    )
    create_span_subelement(
        property_descriptor.type or 'Any',
        f'{HTML_CLASS_BASE}-type',
        code
    )
    create_span_subelement(
        ' = ...\n',
        f'{HTML_CLASS_BASE}-punctuation',
        code
    )
    # create_subelement('br', [], code)

    if property_descriptor.is_settable:
        code = create_subelement(
            'code',
            [('class', f'{HTML_CLASS_BASE}-function-signature')],
            container
        )
        create_span_subelement(
            property_descriptor.qual_name,
            f'{HTML_CLASS_BASE}-type',
            code
        )
        create_span_subelement(
            ' -> ',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        create_span_subelement(
            property_descriptor.type or 'Any',
            f'{HTML_CLASS_BASE}-type',
            code
        )
        create_span_subelement(
            '\n',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        # create_subelement('br', [], code)

    if property_descriptor.is_deletable:
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
            property_descriptor.qual_name,
            f'{HTML_CLASS_BASE}-type',
            code
        )
        create_span_subelement(
            '\n',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        # create_subelement('br', [], code)

    render_raises(property_descriptor.raises, container, md)
    render_description(property_descriptor.description, container, md)
    render_examples(property_descriptor.examples, container, md)

    return container

def render_class(
        class_descriptor: ClassDescriptor,
        md: Markdown,
        parent: etree.Element
) -> etree.Element:

    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-class')],
        parent
    )

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
    container = create_subelement(
        'code',
        [('class', f'{HTML_CLASS_BASE}-function-signature')],
        parent
    )

    if function_descriptor.is_async:
        create_span_subelement(
            "async ",
            f'{HTML_CLASS_BASE}-function-punctuation',
            container
        )

    create_span_subelement(
        function_descriptor.name,
        f'{HTML_CLASS_BASE}-function-name',
        container
    )

    create_span_subelement('(', f'{HTML_CLASS_BASE}-punctuation', container)

    is_first = True
    for argument in function_descriptor.arguments:
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
            argument.name,
            f'{HTML_CLASS_BASE}-function-var',
            container
        )

        if argument.type:
            create_span_subelement(
                ': ', f'{HTML_CLASS_BASE}-punctuation', container)
            create_span_subelement(
                argument.type,
                f'{HTML_CLASS_BASE}-variable-type',
                container
            )

    create_span_subelement(')', f'{HTML_CLASS_BASE}-punctuation', container)

    if function_descriptor.return_type:
        create_span_subelement(
            ' -> ', f'{HTML_CLASS_BASE}-punctuation', container)
        create_span_subelement(
            function_descriptor.return_type,
            f'{HTML_CLASS_BASE}-variable-type',
            container
        )


def render_parameters(
        arguments: List[ArgumentDescriptor],
        parent: etree.Element,
        md: Markdown
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

    for argument in arguments:

        parameter_container = create_subelement(
            'div',
            [('class', f'{HTML_CLASS_BASE}-function-parameters')],
            container
        )

        create_text_subelement(
            'var',
            argument.name,
            f'{HTML_CLASS_BASE}-function-var',
            parameter_container
        )

        if argument.type:
            create_span_subelement(
                ': ',
                f'{HTML_CLASS_BASE}-punctuation',
                parameter_container
            )
            create_span_subelement(
                argument.type,
                f'{HTML_CLASS_BASE}-variable-type',
                parameter_container
            )

        if argument.is_optional:
            create_span_subelement(
                ' (optional)',
                f'{HTML_CLASS_BASE}-punctuation',
                parameter_container
            )


        create_subelement('br', [], parameter_container)

        create_text_subelement(
            'p',
            md.convert(argument.description or ''),
            f'{HTML_CLASS_BASE}-function-param',
            parameter_container
        )

    return container


def render_returns(
        function_descriptor: FunctionDescriptor,
        parent: etree.Element,
        md: Markdown
) -> etree.Element:

    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-function-returns')],
        parent
    )

    if not function_descriptor.return_type or function_descriptor.return_type in ('None', 'typing.None'):
        return container

    create_text_subelement(
        'h3',
        'Yields' if function_descriptor.is_generator else 'Returns',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    create_span_subelement(
        function_descriptor.return_type,
        f'{HTML_CLASS_BASE}-variable-type',
        container
    )
    create_span_subelement(
        ': ',
        f'{HTML_CLASS_BASE}-punctuation',
        container
    )

    description = function_descriptor.return_description or ''
    text = md.convert(description)
    if text.startswith('<p>') and text.endswith('</p>'):
        text = text[3:-4]
    create_span_subelement(
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

    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-function-raises')],
        parent
    )
    if not raises:
        return container

    create_text_subelement(
        'h3',
        'Raises',
        f'{HTML_CLASS_BASE}-function-header',
        container
    )

    for error in raises:
        error_container = create_subelement(
            'p',
            [('class', f'{HTML_CLASS_BASE}-function-raises')],
            container
        )

        create_span_subelement(
            error.type,
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
    container = create_subelement(
        'p',
        [('class', f'{HTML_CLASS_BASE}-function')],
        parent
    )

    return render_function_in_container(function_descriptor, md, container)


def render_module(
        module_descriptor: ModuleDescriptor,
        md,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-module')],
        parent
    )

    render_title(module_descriptor.name, 'module', container)
    render_meta_data(None, module_descriptor.package, module_descriptor.file, container)
    render_summary(module_descriptor.summary, container, md)
    render_attributes(module_descriptor.attributes, md, container)
    render_description(module_descriptor.description, container, md)
    render_examples(module_descriptor.examples, container, md)

    return container
