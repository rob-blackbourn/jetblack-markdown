"""A markdown extension for creating documentation"""

from markdown import Markdown
from markdown.extensions import Extension

from .latex2mathml_processor import Latex2MathMLInlineProcessor, Latex2MathMLBlockProcessor


__all__ = [
    "Latex2MathMLExtension",
    "makeExtension"
]


class Latex2MathMLExtension(Extension):

    # RE = r'\$([^\$]+)\$'
    # RE = r'\\((.*)\\)'
    RE = r'(?:(?<!\\)((?:\\{2})+)(?=\$)|(?<!\\)(\$)((?:\\.|[^\\$])+?)(?:\$))'

    def __init__(self, *args, **kwargs) -> None:
        self.config = {}
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        md.inlinePatterns.register(
            Latex2MathMLInlineProcessor(
                self.RE,
                md,
            ),
            'mathml',
            175
        )
        md.parser.blockprocessors.register(
            Latex2MathMLBlockProcessor(md.parser),
            'mathml',
            175
        )


# pylint: disable=invalid-name
def makeExtension(*args, **kwargs) -> Extension:
    return Latex2MathMLExtension(*args, **kwargs)
