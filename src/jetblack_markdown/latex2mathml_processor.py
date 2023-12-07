"""A mathml markdown processor"""

from functools import partial
import re
from typing import (
    List,
    Optional,
    Tuple,
    Union
)
import xml.etree.ElementTree as etree
from xml.etree.cElementTree import Element, SubElement

from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.blockparser import BlockParser
from markdown.blockprocessors import BlockProcessor

from latex2mathml.converter import convert_to_element

HTML_CLASS = "latex2mathml"


class Latex2MathMLInlineProcessor(InlineProcessor):
    """An inline processor for Python documentation"""

    def __init__(
            self,
            pattern,
            md: Optional[Markdown] = None,
    ) -> None:
        super().__init__(pattern, md=md)

    # pylint: disable=arguments-differ
    def handleMatch(
            self,
            matches: re.Match,
            data: str
    ) -> Union[Tuple[etree.Element, int, int], Tuple[None, None, None]]:
        latex = matches.group(3)
        element = convert_to_element(latex)
        start = matches.start(0)
        end = matches.end(0)
        return element, start, end


class Latex2MathMLBlockProcessor(BlockProcessor):

    def __init__(self, parser: BlockParser):
        super().__init__(parser)
        self._pattern = re.compile(
            r'(?P<dollar>[$]{2})(?P<math>((?:\\.|[^\\])+?))(?P=dollar)'
        )
        self._match: Optional[re.Match[str]] = None

    def test(self, parent: Element, block: str) -> bool:
        self._match = self._pattern.match(block)
        return self._match is not None

    def run(self, parent: Element, blocks: List[str]) -> Optional[bool]:

        assert self._match is not None
        latex = self._match.group('math')
        if not latex:
            return False

        element = convert_to_element(
            latex.strip(),
            display='block',
            parent=parent
        )
        element.set("class", HTML_CLASS)

        blocks.pop(0)

        return True
