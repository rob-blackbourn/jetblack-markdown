"""Module rendering"""

from typing import (
    Any
)

from markdown.util import etree

from .constants import HTML_CLASS_BASE
from .utils import (
    create_subelement,
)
from .renderers import (
    render_title,
    render_summary,
    render_description,
    render_examples,
    render_meta_data,
    render_attributes
)

from .metadata import ModuleDescriptor
