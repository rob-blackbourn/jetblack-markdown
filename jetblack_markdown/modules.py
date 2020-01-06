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
    render_description,
    render_examples,
    render_meta_data
)

from .metadata import ModuleDescriptor, ArgumentDescriptor

def _render_module_meta_data_obj(module: Any, parent: etree.Element) -> etree.Element:
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
            md.convert(attribute.description),
            f'{HTML_CLASS_BASE}-class-attr',
            attr_container
        )

    return container

def render_module(
        obj: Any,
        md,
        parent: etree.Element
) -> etree.Element:
    container = create_subelement(
        'div',
        [('class', f'{HTML_CLASS_BASE}-module')],
        parent
    )

    module_descriptor = ModuleDescriptor.create(obj)

    render_title(module_descriptor.name, 'module', container)
    render_meta_data(None, module_descriptor.package, module_descriptor.file, container)
    render_summary(module_descriptor.summary, container, md)
    render_module_attributes(module_descriptor.attributes, md, container)
    render_description(module_descriptor.description, container, md)
    render_examples(module_descriptor.examples, container, md)

    return container
