"""A Latex to MathML markdown processor"""

from functools import partial
import re
from typing import (
    List,
    Optional,
    Tuple,
    Union
)
import xml.etree.ElementTree as etree
from xml.etree.cElementTree import Element

from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.blockparser import BlockParser
from markdown.blockprocessors import BlockProcessor

from latex2mathml.converter import convert_to_element

HTML_CLASS = "latex2mathml"


class Latex2MathMLInlineProcessor(InlineProcessor):
    """An inline processor for converting Latex to MathML"""

    def __init__(
            self,
            pattern,
            md: Optional[Markdown] = None,
    ) -> None:
        super().__init__(pattern, md=md)

    def handleMatch(
            self,
            matches: re.Match,
            data: str
    ) -> Tuple[Optional[Union[etree.Element, str]], Optional[int], Optional[int]]:
        latex = matches.group(1)
        if not latex:
            return None, None, None

        element = convert_to_element(latex.strip())
        element.set("class", HTML_CLASS)
        del element.attrib['xmlns']

        start = matches.start(0)
        end = matches.end(0)
        return element, start, end


class Latex2MathMLBlockProcessor(BlockProcessor):
    """An block processor for converting Latex to MathML"""

    def __init__(self, parser: BlockParser):
        super().__init__(parser)
        self._pattern = re.compile(
            r' *\$\$\n(.*)\n\$\$ *'
        )
        self._match: Optional[re.Match[str]] = None

    def test(self, parent: Element, block: str) -> bool:
        self._match = self._pattern.match(block)
        return self._match is not None

    def run(self, parent: Element, blocks: List[str]) -> Optional[bool]:

        assert self._match is not None
        latex = self._match.group(1)
        if not latex:
            return False

        element = convert_to_element(
            latex.strip(),
            display='block',
            parent=parent
        )
        element.set("class", HTML_CLASS)
        del element.attrib['xmlns']

        blocks.pop(0)

        return True
