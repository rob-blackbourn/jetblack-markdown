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
