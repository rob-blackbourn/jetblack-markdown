"""A sample extension"""

import importlib
import inspect
import re
from typing import (
    Any,
    List,
    Optional,
    Mapping,
    Set,
    Tuple
)

import docstring_parser
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.util import etree

from .functions import render_function

DOCSTRING_RE = r'@\[([^\]]+)\]'
DEFAULT_INSTRUCTION_SET = {'shallow'}
HTML_CLASS_BASE = 'jetblack'


def import_from_string(import_str: str) -> Any:
    """Import some python object from a given string

    :param import_str: The import string
    :type import_str: str
    :return: The imported object
    :rtype: Any
    """
    module_str, _, attr_str = import_str.rpartition(".")

    try:
        module = importlib.import_module(module_str)
    except ImportError as exc:
        module_name = module_str.split(".", 1)[0]
        if exc.name != module_name:
            raise exc from None
        raise ValueError(f"Could not import module {module_str!r}.")

    try:
        return getattr(module, attr_str)
    except AttributeError as exc:
        raise ValueError(
            f"Attribute {attr_str!r} not found in module {module_str!r}.")


class MyPattern(InlineProcessor):
    """An inline processort for Python documentation"""

    def handleMatch(
            self,
            matches: re.Match,
            data: str
    ) -> Tuple[etree.Element, int, int]:
        """Handle a match

        :param matches: The regular expression match result
        :type matches: re.Matche
        :param data: The matched text
        :type data: str
        :return: The element to insert and the start and end index
        :rtype: Tuple[Element, int, int]
        """
        text = matches.group(1)
        import_str, sep, instructions = text.partition(':')
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
            pass
        elif inspect.isclass(obj):
            pass
        elif inspect.isfunction(obj):
            return render_function(obj, instructions)
        else:
            pass

        element = etree.Element('span')
        element.text = 'hello'
        return element

    def _render_class(self, obj: Any, instructions: Set[str]) -> etree.Element:
        pass

    def _render_module(self, obj: Any, instructions: Set[str]) -> etree.Element:
        pass


class MyExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            MyPattern(DOCSTRING_RE, md), 'jetblack_markdown', 175)


def makeExtension():
    return MyExtension()


def sample_func(
        arg1: int,
        arg2: Optional[float],
        arg3=Mapping[str, Any]
) -> Optional[Tuple[List[str], Any]]:
    """A sample function

    A function that does nothing.

    Args:
        arg1 (int): The first arg
        arg2 (Optional[float]): The second arg
        arg3 (Mapping[str, Any], optional): The third arg. Defaults to Mapping[str, Any].

    Raises:
        RuntimeError: When arg1 is 0

    Returns:
        Optional[Tuple[List[str], Any]]: Some stuff
    """
    if not arg1:
        raise RuntimeError('arg1 cannot be zero')
    return None


if __name__ == '__main__':
    pattern = re.compile(r'@\[([^\]]+)\]')
    matches = pattern.match("@[foo.bar:deep]")
    print(matches)
