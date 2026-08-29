"""A Latex to MathML markdown processor"""

import re
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import Element

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
            md: Markdown | None = None,
    ) -> None:
        super().__init__(pattern, md=md)

    def handleMatch(  # type: ignore
            self,
            m: re.Match[str],
            data: str
    ) -> tuple[etree.Element | str | None, int | None, int | None]:
        latex = m.group(1)
        if not latex:
            return None, None, None

        element = convert_to_element(latex.strip())
        element.set("class", HTML_CLASS)
        del element.attrib['xmlns']

        start = m.start(0)
        end = m.end(0)
        return element, start, end


class Latex2MathMLBlockProcessor(BlockProcessor):
    """An block processor for converting Latex to MathML"""

    def __init__(self, parser: BlockParser):
        super().__init__(parser)
        self._pattern = re.compile(
            r' *\$\$\n(.*)\n\$\$ *'
        )
        self._match: re.Match[str] | None = None

    def test(self, parent: Element, block: str) -> bool:
        self._match = self._pattern.match(block)
        return self._match is not None

    def run(self, parent: Element, blocks: list[str]) -> bool | None:

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
