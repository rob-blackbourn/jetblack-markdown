"""Module rendering"""

from typing import (
    Any,
    List
)

from markdown import Markdown
from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .utils import (
    create_subelement,
    create_span_subelement,
    create_text_subelement
)
from .renderers import (
    render_title,
    render_summary,
    render_meta_data,
    render_description,
    render_examples
)
from .functions import (
    _render_signature,
    _render_parameters,
    _render_raises,
    create_function
)
from .metadata import (
    ArgumentDescriptor,
    PropertyDescriptor,
    ClassDescriptor
)

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

    _render_raises(property_descriptor.raises, container, md)
    render_description(property_descriptor.description, container, md)
    render_examples(property_descriptor.examples, container, md)

    return container

def render_class_attributes(
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
            [('class', f'{HTML_CLASS_BASE}-class-attributes')],
            container
        )

        create_text_subelement(
            'var',
            attribute.name,
            f'{HTML_CLASS_BASE}-class-attr',
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
                f'{HTML_CLASS_BASE}-variable-type',
                attr_container
            )

        create_subelement('br', [], attr_container)

        create_text_subelement(
            'p',
            md.convert(attribute.description or ''),
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

    class_descriptor = ClassDescriptor.create(
        obj,
        class_from_init,
        ignore_dunder,
        ignore_private
    )

    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-class')],
        parent
    )

    render_title(class_descriptor.name, 'class', container)
    render_meta_data(class_descriptor.module, class_descriptor.package, class_descriptor.file, container)
    render_summary(class_descriptor.summary, container, md)
    _render_signature(class_descriptor.constructor, container)
    _render_parameters(class_descriptor.constructor.arguments, container, md)
    render_class_attributes(class_descriptor.attributes, md, container)
    _render_raises(class_descriptor.constructor.raises, container, md)
    render_description(class_descriptor.description, container, md)
    render_examples(class_descriptor.examples, container, md)
    for prop in class_descriptor.properties:
        render_property(prop, md, container)
    for method in class_descriptor.methods:
        create_function(method, md, container)

    return container

