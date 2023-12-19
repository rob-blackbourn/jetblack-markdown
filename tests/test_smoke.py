"""A test placeholder"""

import xml.etree.ElementTree as etree

import markdown

from jetblack_markdown.autodoc import AutodocExtension
from jetblack_markdown.latex2mathml import Latex2MathMLExtension


def test_smoketest():
    content = """
An inline formula looks like: $x=\frac{-b\pm\sqrt{b^2-4ac} }{2a}$.

A block looks like:

$$
x=\frac{-b\pm\sqrt{b^2-4ac} }{2a}
$$

The outer `<math>` tag has the HTML class `"latex2mathml"`.

Here is some API documentation.

@[jetblack_markdown.latex2mathml]
"""
    extensions = [
        AutodocExtension(class_from_init=True),
        Latex2MathMLExtension()
    ]
    output = markdown.markdown(content, extensions=extensions)
    assert output is not None


def test_etree():
    tree = etree.fromstring('<div>Hello</div>')
    print(tree)
