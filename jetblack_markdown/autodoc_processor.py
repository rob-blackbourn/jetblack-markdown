"""A sample extension"""

import importlib
import inspect
import re
from typing import (
    Any,
    Set,
    Tuple
)

from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .functions import render_function
from .modules import render_module
from .classes import render_class
from .utils import import_from_string

DEFAULT_INSTRUCTION_SET = {'shallow'}

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
        self.class_from_init = class_from_init
        self.ignore_dunder = ignore_dunder
        self.ignore_private = ignore_private
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

        container = etree.Element('div')
        container.set('class', f'{HTML_CLASS_BASE}-documentation')

        if inspect.ismodule(obj):
            render_module(obj, self.md, container)
        elif inspect.isclass(obj):
            render_class(
                obj,
                self.md,
                self.class_from_init,
                self.ignore_dunder,
                self.ignore_private,
                container
            )
        elif inspect.isfunction(obj):
            render_function(obj, self.md, container)

        return container
