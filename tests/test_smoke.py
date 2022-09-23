"""A test placeholder"""

import xml.etree.ElementTree as etree

import markdown

from jetblack_markdown.autodoc import AutodocExtension


def test_smoketest():
    content = """

@[jetblack_markdown]

Something else
"""
    extension = AutodocExtension(class_from_init=True)
    output = markdown.markdown(content, extensions=[extension])
    assert output is not None


def test_etree():
    tree = etree.fromstring('<div>Hello</div>')
    print(tree)
