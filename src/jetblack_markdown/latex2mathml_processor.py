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
from markdown.blockprocessors import BlockProcessor

from latex2mathml.converter import _convert_group
from latex2mathml.walker import walk

HTML_CLASS = "latex2mathml"


def convert(
        latex: str,
        xmlns: str = "http://www.w3.org/1998/Math/MathML",
        display: str = "inline",
        parent: Optional[Element] = None
) -> Element:
    tag = 'math'
    attrib = {
        'class': HTML_CLASS,
        'xmlns': xmlns,
        'display': display
    }
    math = (
        Element(tag, attrib)
        if parent is None
        else SubElement(parent, tag, attrib)
    )
    row = SubElement(math, "mrow")
    _convert_group(iter(walk(latex)), row)
    return math


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
        latex = matches.group(1)
        element = convert(latex)
        start = matches.start(0)
        end = matches.end(0)
        return element, start, end


class Latex2MathMLBlockProcessor(BlockProcessor):

    RE_START = r"^ *\${2} *\n"  # Start line, e.g., `    $$  `
    RE_END = r"\n *\${2}\s*$"  # End line, e.g., `$$$\n`

    def test(self, parent: Element, block: str) -> bool:
        return re.match(self.RE_START, block) is not None

    def run(self, parent: Element, blocks: List[str]) -> Optional[bool]:
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_START, '', blocks[0])

        # Find block with ending fence.
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_END, block):
                # Remove fence.
                blocks[block_num] = re.sub(self.RE_END, '', block)
                # Convert as a child of the parent element.
                element = convert(
                    ' '.join(blocks[0:block_num + 1]),
                    display='block',
                    parent=parent
                )
                element.set("class", HTML_CLASS)
                # Remove blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True

        # No closing marker! Restore and do nothing.
        blocks[0] = original_block
        return False
