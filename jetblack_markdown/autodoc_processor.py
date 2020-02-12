"""A sample extension"""

import inspect
import re
from typing import (
    Any,
    Optional,
    Tuple
)

from jinja2 import (
    Environment,
    BaseLoader,
    PackageLoader,
    FileSystemLoader,
    select_autoescape
)
from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.util import etree

from .metadata import (
    Descriptor,
    ModuleDescriptor,
    CallableDescriptor,
    ClassDescriptor
)
from .utils import import_from_string


class AutodocInlineProcessor(InlineProcessor):
    """An inline processort for Python documentation"""

    def __init__(
            self,
            pattern,
            md: Markdown = None,
            *,
            class_from_init: bool = True,
            ignore_dunder: bool = True,
            ignore_private: bool = True,
            ignore_all: bool = False,
            ignore_inherited: bool = True,
            prefer_docstring: bool = True,
            follow_module_tree: bool = False,
            template_folder: Optional[str] = None,
            template_file: str = "main.jinja2"
    ) -> None:
        """An inline processor for Python documentation

        Args:
            pattern ([type]): The regular expression to match
            md (Markdown, optional): The markdown object provided by the
                extension. Defaults to None.
            class_from_init (bool, optional): If True use the docstring from
                the &#95;&#95;init&#95;&#95; function for classes. Defaults to
                True.
            ignore_dunder (bool, optional): If True ignore
                &#95;&#95;XXX&#95;&#95; functions. Defaults to True.
            ignore_private (bool, optional): If True ignore methods
                (those prefixed &#95;XXX). Defaults to True.
            ignore_all (bool): If True ignore the &#95;&#95;all&#95;&#95; member.
            ignore_inherited (bool): If True ignore inherited members.
            prefer_docstring (bool): If true prefer the docstring.
            follow_module_tree (bool): If true follow the module tree.
            template_folder (Optional[str], optional): The template folder,
                Defaults to None.
            template_file (Optional[str], optional): The template file to use,
                Defaults to "main.jinja2".
        """
        self.class_from_init = class_from_init
        self.ignore_dunder = ignore_dunder
        self.ignore_private = ignore_private
        self.ignore_all = ignore_all
        self.ignore_inherited = ignore_inherited
        self.follow_module_tree = follow_module_tree
        self.prefer_docstring = prefer_docstring
        if template_folder:
            loader: BaseLoader = FileSystemLoader(template_folder)
        else:
            loader = PackageLoader('jetblack_markdown', 'templates')
        self.env = Environment(
            loader=loader,
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.env.filters['md_format'] = self._md_format
        self.template = self.env.get_template(template_file)
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
        import_str = matches.group(1)

        element = self._render(import_str)
        start = matches.start(0)
        end = matches.end(0)
        return element, start, end

    def _render(self, import_str: str) -> etree.Element:
        obj = import_from_string(import_str)
        descriptor = self._make_descriptor(obj)
        html = self.template.render(
            obj=descriptor
        )
        return etree.fromstring(html)

    def _make_descriptor(self, obj: Any) -> Descriptor:
        if inspect.ismodule(obj):
            return ModuleDescriptor.create(
                obj,
                self.class_from_init,
                self.ignore_dunder,
                self.ignore_private,
                self.ignore_all,
                self.ignore_inherited,
                self.prefer_docstring,
                self.follow_module_tree
            )
        elif inspect.isclass(obj):
            return ClassDescriptor.create(
                obj,
                self.class_from_init,
                self.ignore_dunder,
                self.ignore_private,
                self.ignore_inherited,
                prefer_docstring=self.prefer_docstring
            )
        elif inspect.isfunction(obj):
            return CallableDescriptor.create(
                obj,
                prefer_docstring=self.prefer_docstring
            )
        else:
            raise RuntimeError("Unhandled descriptor")

    def _md_format(self, text: str) -> str:
        md = Markdown(extensions=self.md.registeredExtensions)
        result = md.convert(text)
        return result
