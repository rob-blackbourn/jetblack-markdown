"""Utilities"""

import importlib
from inspect import Parameter
import re
from typing import Any, Optional, Union
import xml.etree.ElementTree as etree

from docstring_parser import Docstring, DocstringParam, DocstringReturns


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
        raise ValueError(f"Could not import module {module_str!r}.") from exc

    if not attr_str:
        return module

    try:
        return getattr(module, attr_str)
    except AttributeError as exc:
        raise ValueError(
            f"Attribute {attr_str!r} not found in module {module_str!r}."
        ) from exc


def add_tag(tag: str, class_name: Optional[str], parent: etree.Element) -> etree.Element:
    element = etree.SubElement(parent, tag)
    if class_name:
        element.set('class', class_name)
    return element


def add_text_tag(tag: str, text: str, klass: Optional[str], parent: etree.Element) -> etree.Element:
    element = add_tag(tag, klass, parent)
    element.text = text
    return element


def add_span_tag(text: str, klass: Optional[str], parent: etree.Element) -> etree.Element:
    return add_text_tag('span', text, klass, parent)


def find_docstring_param(name: str, docstring: Docstring) -> Optional[DocstringParam]:
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
    """Get the type name

    Args:
        annotation (Any): The type annotation
        docstring_param (Optional[Union[DocstringParam, DocstringReturns]]):
            The docstring param

    Returns:
        str: The type description
    """
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
