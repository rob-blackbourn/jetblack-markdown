"""Module rendering"""

from typing import (
    Any,
    List
)

from markdown import Markdown
from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .utils import (
    create_subelement,
    create_span_subelement,
    create_text_subelement
)
from .renderers import (
    render_title,
    render_summary,
    render_meta_data,
    render_description,
    render_examples,
    render_attributes
)
from .functions import (
    _render_signature,
    _render_parameters,
    _render_raises,
    render_function_in_container
)
from .metadata import (
    ArgumentDescriptor,
    PropertyDescriptor,
    ClassDescriptor
)


