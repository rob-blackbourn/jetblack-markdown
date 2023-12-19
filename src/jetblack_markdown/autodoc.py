"""A markdown extension for creating documentation"""

from markdown import Markdown
from markdown.extensions import Extension

from .autodoc_processor import AutodocBlockProcessor

_DOCSTRING_RE = r'@\[([^\]]+)\]'

__all__ = [
    "AutodocExtension",
    "makeExtension"
]


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
            'ignore_inherited': [True, 'Ignore inherited members'],
            'prefer_docstring': [True, 'Prefer the docstring'],
            'follow_module_tree': [False, 'Follow the module tree'],
            'template_folder': ['', 'The template folder'],
            'template_file': ['main.jinja2', 'The template file to use'],
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        class_from_init = self.getConfig('class_from_init')
        ignore_dunder = self.getConfig('ignore_dunder')
        ignore_private = self.getConfig('ignore_private')
        ignore_all = self.getConfig('ignore_all')
        ignore_inherited = self.getConfig('ignore_inherited')
        prefer_docstring = self.getConfig('prefer_docstring')
        follow_module_tree = self.getConfig('follow_module_tree')
        template_folder = self.getConfig('template_folder')
        template_file = self.getConfig('template_file')
        md.parser.blockprocessors.register(
            AutodocBlockProcessor(
                md.parser,
                class_from_init=class_from_init,
                ignore_dunder=ignore_dunder,
                ignore_private=ignore_private,
                ignore_all=ignore_all,
                ignore_inherited=ignore_inherited,
                prefer_docstring=prefer_docstring,
                follow_module_tree=follow_module_tree,
                template_folder=template_folder,
                template_file=template_file
            ),
            'autodoc',
            200
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
            "jetblack_markdown.autodoc",
        ])
    print(output)
    ```

    Args:
        *args: Positional arguments from the markdown processor
        **kwargs: Keyword arguments from the markdown processor

    Returns:
        Extension: The markdown extension
    """
    return AutodocExtension(*args, **kwargs)
