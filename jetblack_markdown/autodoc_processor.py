"""A sample extension"""

import inspect
import re
from typing import (
    Any,
    Tuple
)

from jinja2 import Environment, PackageLoader, select_autoescape
from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .metadata import (
    Descriptor,
    ModuleDescriptor,
    CallableDescriptor,
    ClassDescriptor
)
from .utils import import_from_string


class AutodocInlineProcessor(InlineProcessor):
    """An inline processort for Python documentation"""

    def __init__(
            self,
            pattern,
            md: Markdown = None,
            class_from_init: bool = True,
            ignore_dunder: bool = True,
            ignore_private: bool = True
    ) -> None:
        """An inline processor for Python documentation

        Args:
            pattern ([type]): The regular expression to match
            md (Markdown, optional): The markdown object provided by the
                extension. Defaults to None.
            class_from_init (bool, optional): If True use the docstring from
                the &#95;&#95;init&#95;&#95; function for classes. Defaults to
                True.
            ignore_dunder (bool, optional): If True ignore
                &#95;&#95;XXX&#95;&#95; functions. Defaults to True.
            ignore_private (bool, optional): If True ignore private methods
                (those prefixed &#95;XXX). Defaults to True.
        """
        self.class_from_init = class_from_init
        self.ignore_dunder = ignore_dunder
        self.ignore_private = ignore_private
        self.env = Environment(
            loader=PackageLoader('jetblack_markdown', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.template = self.env.get_template("render.jinja2")
        super().__init__(pattern, md=md)

    # pylint: disable=arguments-differ
    def handleMatch(
            self,
            matches: re.Match,
            data: str
    ) -> Tuple[etree.Element, int, int]:
        """Handle a match

        Args:
            matches (re.Match): The regular expression match result
            data (str): The matched text

        Returns:
            Tuple[etree.Element, int, int]: The element to insert and the start
                and end index
        """
        import_str = matches.group(1)
        obj = import_from_string(import_str)

        element = self._render(obj)
        start = matches.start(0)
        end = matches.end(0)
        return element, start, end

    def _render(self, obj: Any) -> etree.Element:

        parent = etree.Element('div')
        parent.set('class', f'{HTML_CLASS_BASE}-documentation')

        descriptor = self._make_descriptor(obj)

        html = self.template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            obj=descriptor
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container

    def _make_descriptor(self, obj: Any) -> Descriptor:
        if inspect.ismodule(obj):
            return ModuleDescriptor.create(obj)
        elif inspect.isclass(obj):
            return ClassDescriptor.create(
                obj,
                self.class_from_init,
                self.ignore_dunder,
                self.ignore_private
            )
        elif inspect.isfunction(obj):
            return CallableDescriptor.create(obj)
        else:
            raise RuntimeError("Unhandled descriptor")
