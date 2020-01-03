"""A sample extension"""

import importlib
import inspect
import re
from typing import (
    Any,
    Dict,
    Optional,
    Set,
    Tuple
)

from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.util import etree

from .functions import render_function
from .modules import render_module
from .classes import render_class

DOCSTRING_RE = r'@\[([^\]]+)\]'
DEFAULT_INSTRUCTION_SET = {'shallow'}
HTML_CLASS_BASE = 'jetblack'


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
        text = matches.group(1)
        import_str, _sep, instructions = text.partition('!')
        obj = import_from_string(import_str)
        if not instructions:
            instruction_set = DEFAULT_INSTRUCTION_SET
        else:
            instruction_set = {
                instruction.strip()
                for instruction in instructions.split(',')
            }

        element = self._render_obj(obj, instruction_set)
        start = matches.start(0)
        end = matches.end(0)
        return element, start, end

    def _render_obj(self, obj: Any, instructions: Set[str]) -> etree.Element:
        if inspect.ismodule(obj):
            return render_module(obj, instructions, self.md)
        elif inspect.isclass(obj):
            return render_class(
                obj,
                instructions,
                self.md,
                self.class_from_init,
                self.ignore_dunder,
                self.ignore_private
            )
        elif inspect.isfunction(obj):
            return render_function(obj, instructions, self.md)
        else:
            pass

        element = etree.Element('span')
        element.text = 'hello'
        return element

    def _render_class(self, obj: Any, instructions: Set[str]) -> etree.Element:
        pass

    def _render_module(self, obj: Any, instructions: Set[str]) -> etree.Element:
        pass


class AutodocExtension(Extension):
    """The autodoc extension.

    Reference as "jetblack_markdown.autodoc"
    """

    def __init__(self, *args, **kwargs) -> None:
        self.config = {
            'class_from_init': [False, 'Class documentation is on __init__'],
            'ignore_dunder': [True, 'Ignore dunder methods'],
            'ignore_private': [True, 'Ignore private methods'],
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        class_from_init = self.getConfig('class_from_init')
        ignore_dunder = self.getConfig('ignore_dunder')
        ignore_private = self.getConfig('ignore_private')
        md.inlinePatterns.register(
            AutodocInlineProcessor(
                DOCSTRING_RE,
                md,
                class_from_init,
                ignore_dunder,
                ignore_private
            ),
            'autodoc',
            175
        )


# pylint: disable=invalid-name
def makeExtension(*args, **kwargs) -> Extension:
    """Make the extension

    This hook function get picked up by the markdown processor when the
    extension is listed

    Returns:
        Extension: The extension
    """
    return AutodocExtension(*args, **kwargs)
