"""A markdown extension for creating documentation"""

from markdown import Markdown
from markdown.extensions import Extension

from .autodoc_processor import AutodocInlineProcessor

DOCSTRING_RE = r'@\[([^\]]+)\]'


class AutodocExtension(Extension):
    """The autodoc extension.

    Reference as "jetblack_markdown.autodoc"
    """

    def __init__(self, *args, **kwargs) -> None:
        self.config = {
            'class_from_init': [False, 'Class documentation is on __init__'],
            'ignore_dunder': [True, 'Ignore dunder methods'],
            'ignore_private': [True, 'Ignore private methods'],
            'ignore_all': [False, 'Ignore the __all__ member'],
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        class_from_init = self.getConfig('class_from_init')
        ignore_dunder = self.getConfig('ignore_dunder')
        ignore_private = self.getConfig('ignore_private')
        ignore_all = self.getConfig('ignore_all')
        md.inlinePatterns.register(
            AutodocInlineProcessor(
                DOCSTRING_RE,
                md,
                class_from_init=class_from_init,
                ignore_dunder=ignore_dunder,
                ignore_private=ignore_private,
                ignore_all=ignore_all
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
