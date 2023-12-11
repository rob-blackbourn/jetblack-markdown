r"""A Latex to MathML markdown extension.

Documentation can be written inline like this: $ x=\frac{-b\pm\sqrt{b^2-4ac} }{2a} $.

Or in a block style:

$$
x=\frac{-b\pm\sqrt{b^2-4ac} }{2a}
$$
"""

from markdown import Markdown
from markdown.extensions import Extension

from .latex2mathml_processor import Latex2MathMLInlineProcessor, Latex2MathMLBlockProcessor


__all__ = [
    "Latex2MathMLExtension",
    "makeExtension"
]


class Latex2MathMLExtension(Extension):

    RE = r'\$([^$\n]+)\$'

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
            50
        )
        md.parser.blockprocessors.register(
            Latex2MathMLBlockProcessor(md.parser),
            'mathml',
            50
        )


# pylint: disable=invalid-name
def makeExtension(*args, **kwargs) -> Extension:
    """Make the extension

    This hook *function* gets picked up by the markdown processor when the
    extension is listed

    ```python
    output = markdown.markdown(
        content, extensions=[
            "admonition",
            "codehilite",
            "jetblack_markdown.latex2mathml",
        ])
    print(output)
    ```

    Args:
        *args: Positional arguments from the markdown processor
        **kwargs: Keyword arguments from the markdown processor

    Returns:
        Extension: The markdown extension
    """
    return Latex2MathMLExtension(*args, **kwargs)
