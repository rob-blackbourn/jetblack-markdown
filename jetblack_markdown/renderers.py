"""Rendering functions
"""

import re
from typing import (
    List,
    Optional
)

from jinja2 import Environment, PackageLoader, select_autoescape
from markdown import Markdown
from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .utils import (
    add_tag,
    add_span_tag,
    add_text_tag
)

from .metadata import (
    ArgumentDescriptor,
    PropertyDescriptor,
    RaisesDescriptor,
    CallableDescriptor,
    ClassDescriptor,
    ModuleDescriptor
)

STRIP_WRAPPER_RE = re.compile(r'^<([a-zA-Z][a-zA-Z0-9]*)\b[^>]+>(.*)</\1>$')

class Renderer:

    def __init__(self, md: Markdown) -> None:
        # self.md = md
        self.md = Markdown(extensions=md.registeredExtensions)
        self.env = Environment(
            loader=PackageLoader('jetblack_markdown', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.env.filters['mdconvert'] = self._mdconvert
        self.env.filters['striptag'] = self._striptag


    def _mdconvert(self, value: Optional[str]) -> str:
        return self.md.convert(value) if value else ''

    def _striptag(self, text: str) -> str:
        match = STRIP_WRAPPER_RE.match(text)
        if match:
            return match.group(2)
        return text

    def _mdconvert2(self, value: str) -> str:
        text = self.md.convert(value)
        matches = STRIP_WRAPPER_RE.match(text)
        if matches:
            return matches.group(2)
        return text

    def _render_title(
            self,
            name: str,
            object_type: str,
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("title.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            title_name=name,
            title_object_type=object_type
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container


    def _render_summary(
            self,
            summary: Optional[str],
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("summary.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            summary=summary
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container


    def _render_description(
            self,
            description: Optional[str],
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("description.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            description=description
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container


    def _render_examples(
            self,
            examples: Optional[List[str]],
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("examples.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            examples=examples
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container

    def _render_meta_data(
            self,
            module_name: Optional[str],
            package_name: Optional[str],
            file_name: Optional[str],
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("metadata.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            metadata_module_name=module_name,
            metadata_package_name=package_name,
            metadata_file_name=file_name
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container

    def _render_attributes(
            self,
            descriptors: List[ArgumentDescriptor],
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("attributes.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            attributes=descriptors
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container


    def _render_properties(
            self,
            descriptors: List[PropertyDescriptor],
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("properties.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            properties=descriptors
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container

    def _render_methods(
            self,
            descriptors: List[CallableDescriptor],
            parent: etree.Element
    ) -> etree.Element:
        for descriptor in descriptors:
            self._render_function_in_container(descriptor, parent)
        return parent

    def _render_signature(
            self,
            descriptor: CallableDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("signature.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            is_async=descriptor.is_async,
            callable_name=descriptor.name,
            arguments=descriptor.arguments,
            return_type=descriptor.return_type
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container

    def _render_parameters(
            self,
            descriptors: List[ArgumentDescriptor],
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("parameters.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            arguments=descriptors
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container

    def _render_returns(
            self,
            descriptor: CallableDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("returns.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            return_type=descriptor.return_type,
            is_generator=descriptor.is_generator,
            return_description=descriptor.return_description
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container

    def _render_raises(
            self,
            descriptors: Optional[List[RaisesDescriptor]],
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("raises.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            raises=descriptors
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container


    def _render_function_in_container(
            self,
            descriptor: CallableDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("callable.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            callable_descriptor=descriptor,
            title_name=descriptor.name,
            title_object_type=descriptor.function_type_name,
            metadata_module_name=descriptor.module,
            metadata_package_name=descriptor.package,
            metadata_file_name=descriptor.file,
            summary=descriptor.summary,
            description=descriptor.description,
            is_async=descriptor.is_async,
            is_generator=descriptor.is_generator,
            callable_name=descriptor.name,
            arguments=descriptor.arguments,
            return_type=descriptor.return_type,
            return_description=descriptor.return_description,
            raises=descriptor.raises,
            examples=descriptor.examples
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container

    def render_function(
            self,
            descriptor: CallableDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('p', f'{HTML_CLASS_BASE}-function', parent)
        self._render_function_in_container(descriptor, container)
        return container


    def render_module(
            self,
            descriptor: ModuleDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("module.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            title_name=descriptor.name,
            title_object_type="module",
            metadata_module_name=None,
            metadata_package_name=descriptor.package,
            metadata_file_name=descriptor.file,
            summary=descriptor.summary,
            description=descriptor.description,
            attributes=descriptor.attributes,
            examples=descriptor.examples
        )
        container = etree.fromstring(html)
        parent.append(container)
        return container

    def render_class(
            self,
            descriptor: ClassDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        template = self.env.get_template("class.j2")
        html = template.render(
            CLASS_BASE=HTML_CLASS_BASE,
            title_name=descriptor.name,
            title_object_type="class",
            metadata_module_name=descriptor.module,
            metadata_package_name=descriptor.package,
            metadata_file_name=descriptor.file,
            summary=descriptor.summary,
            description=descriptor.description,
            constructor=descriptor.constructor,
            attributes=descriptor.attributes,
            properties=descriptor.properties,
            methods=descriptor.methods,
            examples=descriptor.examples
        )
        print(html)

        container = add_tag('div', f'{HTML_CLASS_BASE}-class', parent)

        self._render_title(descriptor.name, 'class', container)
        self._render_meta_data(descriptor.module, descriptor.package, descriptor.file, container)
        self._render_summary(descriptor.summary, container)
        self._render_signature(descriptor.constructor, container)
        self._render_parameters(descriptor.constructor.arguments, container)
        self._render_attributes(descriptor.attributes, container)
        self._render_raises(descriptor.constructor.raises, container)
        self._render_description(descriptor.description, container)
        self._render_examples(descriptor.examples, container)
        self._render_properties(descriptor.properties, container)
        self._render_methods(descriptor.methods, container)

        return container
