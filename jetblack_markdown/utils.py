"""Utilities"""

import importlib
from inspect import Parameter
import re
from typing import (
    Any,
    Iterable,
    Optional,
    Tuple,
    Union
)
from docstring_parser import Docstring, DocstringParam, DocstringReturns
from markdown.util import etree

def import_from_string(import_str: str) -> Any:
    """Import some python object from a given string

    Args:
        import_str (str): The import string

    Raises:
        ImportError: If the module could not be imported.
        ValueError: If the module could not be imported.

    Returns:
        Any: The imported object
    """
    module_str, _, attr_str = import_str.partition(":")

    try:
        module = importlib.import_module(module_str)
    except ImportError as exc:
        module_name = module_str.split(".", 1)[0]
        if exc.name != module_name:
            raise exc from None
        raise ValueError(f"Could not import module {module_str!r}.")

    if not attr_str:
        return module

    try:
        return getattr(module, attr_str)
    except AttributeError as exc:
        raise ValueError(
            f"Attribute {attr_str!r} not found in module {module_str!r}.")


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


def find_docstring_param(name: str, docstring: Docstring) -> DocstringParam:
    return next(
        (
            param
            for param in docstring.params
            if param.arg_name == name
        ),
        None
    ) if docstring else None


def get_type_name(
        annotation: Any,
        docstring_param: Optional[Union[DocstringParam, DocstringReturns]]
) -> str:
    type_name = docstring_param.type_name if docstring_param else None
    if type_name:
        return type_name
    if annotation is Parameter.empty:
        return 'Any'

    type_name = getattr(annotation, '__name__', None)
    if not type_name:
        type_name = getattr(annotation, '_', None)
    if not type_name:
        type_name = str(annotation)

    return re.sub(
        r'[^a-zA-Z_]*typing\.([a-zA-Z_][a-zA-Z_0-9]*)',
        r'\1',
        type_name
    )
