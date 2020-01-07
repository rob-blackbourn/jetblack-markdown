"""Rendering functions
"""

from typing import (
    List,
    Optional
)

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

class Renderer:

    def __init__(self, md: Markdown) -> None:
        self.md = md


    def _render_title(
            self,
            name: str,
            object_type: str,
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('div', f'{HTML_CLASS_BASE}-title',parent)
        header = add_tag('h2', f'{HTML_CLASS_BASE}-header', container)
        add_span_tag(name.replace('_', '&lowbar;'), f'{HTML_CLASS_BASE}-name', header)
        add_span_tag(' ', None, header)
        add_span_tag(f'({object_type})', f'{HTML_CLASS_BASE}-object-type', header)

        return container


    def _render_summary(
            self,
            summary: Optional[str],
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('div', f'{HTML_CLASS_BASE}-summary', parent)

        if summary:
            add_text_tag('h3', 'Summary', f'{HTML_CLASS_BASE}-summary', container)
            paragraph = add_tag('p', f'{HTML_CLASS_BASE}-function-summary', container)
            paragraph.text = self.md.convert(summary)

        return container


    def _render_description(
            self,
            description: Optional[str],
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('div', f'{HTML_CLASS_BASE}-description', parent)

        if description:
            add_text_tag('h3', 'Description', f'{HTML_CLASS_BASE}-description', container)
            paragraph = add_tag('p', f'{HTML_CLASS_BASE}-description', container)
            paragraph.text = self.md.convert(description)


    def _render_examples(
            self,
            examples: Optional[List[str]],
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('div', f'{HTML_CLASS_BASE}-examples', parent)

        if not examples:
            return container

        add_text_tag('h3', 'Examples', f'{HTML_CLASS_BASE}-description', container)

        for example in examples:
            paragraph = add_tag('p', None, container)
            paragraph.text = self.md.convert(example)

        return container

    def _render_meta_data(
            self,
            module_name: Optional[str],
            package_name: Optional[str],
            file_name: Optional[str],
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('p', f'{HTML_CLASS_BASE}-metadata', parent)

        if module_name:
            add_text_tag('strong', 'Module:', f'{HTML_CLASS_BASE}-metadata-header', container)
            add_span_tag(' ', None, container)
            add_span_tag(module_name, f'{HTML_CLASS_BASE}-metadata-value', container)
            add_tag('br', None, container)

        if package_name:
            add_text_tag('strong', 'Package: ', f'{HTML_CLASS_BASE}-metadata-header', container)
            add_span_tag(' ', None, container)
            add_span_tag(package_name, f'{HTML_CLASS_BASE}-metadata-value', container)
            add_tag('br', None, container)

        if file_name:
            add_text_tag('strong', 'File', f'{HTML_CLASS_BASE}-metadata-header', container)
            add_span_tag(': ', None, container)
            add_span_tag(file_name, f'{HTML_CLASS_BASE}-metadata-value', container)
            add_tag('br', None, container)

        return container


    def _render_attribute(
            self,
            descriptor: ArgumentDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('div', f'{HTML_CLASS_BASE}-attributes', parent)

        add_text_tag('var', descriptor.name, f'{HTML_CLASS_BASE}-name', container)

        if descriptor.type:
            add_span_tag(': ', f'{HTML_CLASS_BASE}-punctuation', container)
            add_span_tag(descriptor.type, f'{HTML_CLASS_BASE}-vartype', container)

        add_tag('br', None, container)

        description = self.md.convert(descriptor.description or '')
        add_text_tag('p', description, f'{HTML_CLASS_BASE}-description', container)

        return container

    def _render_attributes(
            self,
            descriptors: List[ArgumentDescriptor],
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('div', f'{HTML_CLASS_BASE}-attributes',parent)

        if not descriptors:
            return container

        add_text_tag('h3', 'Attributes', f'{HTML_CLASS_BASE}-description', container)

        for descriptor in descriptors:
            self._render_attribute(descriptor, container)

        return container
        
    def _render_property(
            self,
            descriptor: PropertyDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('div', f'{HTML_CLASS_BASE}-function-raises',parent)

        self._render_title(descriptor.qual_name, "property", container)
        # _render_meta_data_obj(klass, container)

        self._render_summary(descriptor.summary, container)

        code = add_tag('code', f'{HTML_CLASS_BASE}-function-signature', container)

        add_span_tag(
            descriptor.qual_name,
            f'{HTML_CLASS_BASE}-type',
            code
        )
        add_span_tag(
            ': ',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )
        add_span_tag(
            descriptor.type or 'Any',
            f'{HTML_CLASS_BASE}-type',
            code
        )
        add_span_tag(
            ' = ...\n',
            f'{HTML_CLASS_BASE}-punctuation',
            code
        )

        if descriptor.is_settable:
            code = add_tag('code', f'{HTML_CLASS_BASE}-function-signature', container)
            add_span_tag(
                descriptor.qual_name,
                f'{HTML_CLASS_BASE}-type',
                code
            )
            add_span_tag(
                ' -> ',
                f'{HTML_CLASS_BASE}-punctuation',
                code
            )
            add_span_tag(
                descriptor.type or 'Any',
                f'{HTML_CLASS_BASE}-type',
                code
            )
            add_span_tag(
                '\n',
                f'{HTML_CLASS_BASE}-punctuation',
                code
            )

        if descriptor.is_deletable:
            code = add_tag('code', f'{HTML_CLASS_BASE}-function-signature', container)
            add_span_tag(
                'del ',
                f'{HTML_CLASS_BASE}-punctuation',
                code
            )
            add_span_tag(
                descriptor.qual_name,
                f'{HTML_CLASS_BASE}-type',
                code
            )
            add_span_tag(
                '\n',
                f'{HTML_CLASS_BASE}-punctuation',
                code
            )

        self._render_raises(descriptor.raises, container)
        self._render_description(descriptor.description, container)
        self._render_examples(descriptor.examples, container)

        return container

    def _render_properties(
            self,
            descriptors: List[PropertyDescriptor],
            parent: etree.Element
    ) -> etree.Element:
        for descriptor in descriptors:
            self._render_property(descriptor, parent)
        return parent

    def _render_methods(
            self,
            descriptors: List[CallableDescriptor],
            parent: etree.Element
    ) -> etree.Element:
        for descriptor in descriptors:
            self._render_function_in_container(descriptor, parent)
        return parent

    def render_class(
            self,
            descriptor: ClassDescriptor,
            parent: etree.Element
    ) -> etree.Element:

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

    def _render_signature(
            self,
            descriptor: CallableDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('code', f'{HTML_CLASS_BASE}-function-signature', parent)

        if descriptor.is_async:
            add_span_tag(
                "async ",
                f'{HTML_CLASS_BASE}-function-punctuation',
                container
            )

        add_span_tag(
            descriptor.name,
            f'{HTML_CLASS_BASE}-function-name',
            container
        )

        add_span_tag('(', f'{HTML_CLASS_BASE}-punctuation', container)

        is_first = True
        for argument in descriptor.arguments:
            if is_first:
                is_first = False
            else:
                add_span_tag(
                    ', ',
                    f'{HTML_CLASS_BASE}-punctuation',
                    container
                )

            add_text_tag(
                'var',
                argument.name,
                f'{HTML_CLASS_BASE}-function-var',
                container
            )

            if argument.type:
                add_span_tag(
                    ': ', f'{HTML_CLASS_BASE}-punctuation', container)
                add_span_tag(
                    argument.type,
                    f'{HTML_CLASS_BASE}-variable-type',
                    container
                )

        add_span_tag(')', f'{HTML_CLASS_BASE}-punctuation', container)

        if descriptor.return_type:
            add_span_tag(
                ' -> ', f'{HTML_CLASS_BASE}-punctuation', container)
            add_span_tag(
                descriptor.return_type,
                f'{HTML_CLASS_BASE}-variable-type',
                container
            )


    def _render_parameter(
            self,
            descriptor: ArgumentDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('div', f'{HTML_CLASS_BASE}-function-parameters', parent)

        add_text_tag(
            'var',
            descriptor.name,
            f'{HTML_CLASS_BASE}-function-var',
            container
        )

        if descriptor.type:
            add_span_tag(': ', f'{HTML_CLASS_BASE}-punctuation', container)
            add_span_tag(descriptor.type, f'{HTML_CLASS_BASE}-vartype', container)

        if descriptor.is_optional:
            add_span_tag(' (optional)', f'{HTML_CLASS_BASE}-punctuation', container)


        add_tag('br', None, container)

        description = self.md.convert(descriptor.description or '')
        add_text_tag('p', description, f'{HTML_CLASS_BASE}-function-param', container)

        return container

    def _render_parameters(
            self,
            descriptors: List[ArgumentDescriptor],
            parent: etree.Element
    ) -> etree.Element:

        container = add_tag('div', f'{HTML_CLASS_BASE}-function-parameters', parent)
        add_text_tag(
            'h3',
            'Parameters',
            f'{HTML_CLASS_BASE}-function-header',
            container
        )

        for descriptor in descriptors:
            self._render_parameter(descriptor, container)

        return container


    def _render_returns(
            self,
            descriptor: CallableDescriptor,
            parent: etree.Element
    ) -> etree.Element:

        container = add_tag('p', f'{HTML_CLASS_BASE}-function-returns', parent)

        if not descriptor.return_type or descriptor.return_type in ('None', 'typing.None'):
            return container

        add_text_tag(
            'h3',
            'Yields' if descriptor.is_generator else 'Returns',
            f'{HTML_CLASS_BASE}-function-header',
            container
        )

        add_span_tag(
            descriptor.return_type,
            f'{HTML_CLASS_BASE}-variable-type',
            container
        )
        add_span_tag(
            ': ',
            f'{HTML_CLASS_BASE}-punctuation',
            container
        )

        description = descriptor.return_description or ''
        text = self.md.convert(description)
        if text.startswith('<p>') and text.endswith('</p>'):
            text = text[3:-4]
        add_span_tag(
            text,
            f'{HTML_CLASS_BASE}-description',
            container
        )

        return container


    def _render_error(
            self,
            descriptor: RaisesDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('p', f'{HTML_CLASS_BASE}-function-raises', parent)

        add_span_tag(
            descriptor.type,
            f'{HTML_CLASS_BASE}-variable-type',
            container
        )
        add_span_tag(
            ': ',
            f'{HTML_CLASS_BASE}-punctuation',
            container
        )

        text = self.md.convert(descriptor.description)
        if text.startswith('<p>') and text.endswith('</p>'):
            text = text[3:-4]
        add_span_tag(
            text,
            f'{HTML_CLASS_BASE}-function-raises',
            container
        )

        return container

    def _render_raises(
            self,
            descriptors: Optional[List[RaisesDescriptor]],
            parent: etree.Element
    ) -> etree.Element:

        container = add_tag('div', f'{HTML_CLASS_BASE}-function-raises', parent)
        if not descriptors:
            return container

        add_text_tag(
            'h3',
            'Raises',
            f'{HTML_CLASS_BASE}-function-header',
            container
        )

        for descriptor in descriptors:
            self._render_error(descriptor, container)

        return container


    def _render_function_in_container(
            self,
            descriptor: CallableDescriptor,
            container: etree.Element
    ) -> etree.Element:

        self._render_title(descriptor.name, descriptor.function_type_name, container)
        self._render_meta_data(descriptor.module, descriptor.package, descriptor.file, container)
        self._render_summary(descriptor.summary, container)
        self._render_signature(descriptor, container)
        self._render_parameters(descriptor.arguments, container)
        self._render_returns(descriptor, container)
        self._render_raises(descriptor.raises, container)
        self._render_description(descriptor.description, container)
        self._render_examples(descriptor.examples, container)

        return container

    def render_function(
            self,
            descriptor: CallableDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('p', f'{HTML_CLASS_BASE}-function', parent)

        return self._render_function_in_container(descriptor, container)


    def render_module(
            self,
            descriptor: ModuleDescriptor,
            parent: etree.Element
    ) -> etree.Element:
        container = add_tag('div', f'{HTML_CLASS_BASE}-module', parent)

        self._render_title(descriptor.name, 'module', container)
        self._render_meta_data(None, descriptor.package, descriptor.file, container)
        self._render_summary(descriptor.summary, container)
        self._render_attributes(descriptor.attributes, container)
        self._render_description(descriptor.description, container)
        self._render_examples(descriptor.examples, container)

        return container
