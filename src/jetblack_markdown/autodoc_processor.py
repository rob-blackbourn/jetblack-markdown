"""A sample extension"""

import inspect
import re
from typing import Any, List, Optional
import xml.etree.ElementTree as etree
from xml.etree.cElementTree import Element

from jinja2 import (
    Environment,
    BaseLoader,
    PackageLoader,
    FileSystemLoader,
    select_autoescape
)
from markdown.blockparser import BlockParser
from markdown.blockprocessors import BlockProcessor


from .metadata import (
    Descriptor,
    ModuleDescriptor,
    CallableDescriptor,
    ClassDescriptor
)
from .utils import import_from_string


class AutodocBlockProcessor(BlockProcessor):
    """An inline processor for Python documentation"""

    def __init__(
            self,
            parser: BlockParser,
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
        """An inline processor for **Python** documentation

        Args:
            pattern ([type]): The regular expression to match
            md (BlockParser): The parser.
            class_from_init (bool, optional): If True use the docstring from
                the <span>&#95;&#95;</span>init<span>&#95;&#95;</span> function
                for classes. Defaults to True.
            ignore_dunder (bool, optional): If True ignore
                <span>&#95;&#95;</span>XXX<span>&#95;&#95;</span> functions.
                Defaults to True.
            ignore_private (bool, optional): If True ignore private methods
                (those prefixed <span>&#95;</span>XXX). Defaults to True.
            ignore_all (bool): If True ignore the
                <span>&#95;&#95;</span>all<span>&#95;&#95;</span> member.
            ignore_inherited (bool): If True ignore inherited members.
            prefer_docstring (bool): If true prefer the docstring.
            follow_module_tree (bool): If true follow the module tree.
            template_folder (Optional[str], optional): The template folder,
                Defaults to None.
            template_file (Optional[str], optional): The template file to use,
                Defaults to "main.jinja2".
        """
        super().__init__(parser)
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
        self._pattern = re.compile(r'@\[([^\]]+)\]')
        self._match: Optional[re.Match[str]] = None

    def test(self, parent: Element, block: str) -> bool:
        self._match = self._pattern.match(block)
        return self._match is not None

    def run(self, parent: Element, blocks: List[str]) -> Optional[bool]:

        assert self._match is not None
        import_str = self._match.group(1)
        if not import_str:
            return False

        html_text = self._render(import_str)
        element = etree.fromstring(html_text)
        parent.append(element)

        blocks.pop(0)

        return True

    def _render(self, import_str: str) -> str:
        obj = import_from_string(import_str)
        descriptor = self._make_descriptor(obj)
        html_text = self.template.render(
            obj=descriptor
        )
        return html_text

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
        parent = Element("div")
        self.parser.parseChunk(parent, text)
        children = next(iter(parent))
        buf = (
            etree.tostring(children[0])
            if len(children) == 1
            else etree.tostring(parent)
        )
        return buf.decode('utf-8')
