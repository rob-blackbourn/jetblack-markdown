"""Rendering functions
"""

from __future__ import annotations
import inspect
from typing import (
    Any,
    List,
    Optional
)

import docstring_parser
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
    render_description,
    render_examples,
    render_meta_data
)

from .metadata import (
    ArgumentDescriptor,
    FunctionType,
    FunctionDescriptor,
    RaisesDescriptor
)

