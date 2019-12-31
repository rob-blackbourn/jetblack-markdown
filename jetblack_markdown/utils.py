"""Utilities"""

from typing import Iterable, Optional, Tuple
from markdown.util import etree

from .constants import HTML_CLASS_BASE


def create_subelement(tag: str, attrs: Iterable[Tuple[str, str]], parent: etree.Element) -> etree.Element:
    element = etree.SubElement(parent, tag)
    for name, value in attrs:
        element.set(name, value)
    return element


def create_text_subelement(tag: str, text: str, klass: Optional[str], parent: etree.Element) -> etree.Element:
    attrs = [] if klass is None else [('class', klass)]
    element = create_subelement(tag, attrs, parent)
    element.text = text
    return element


def create_span_subelement(text: str, klass: Optional[str], parent: etree.Element) -> etree.Element:
    return create_text_subelement('span', text, klass, parent)
