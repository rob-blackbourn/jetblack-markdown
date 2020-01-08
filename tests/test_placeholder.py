"""A test placeholder"""


import markdown
from markdown.util import etree

from jetblack_markdown.autodoc import AutodocExtension


def test_placeholder():
    content = """

@[jetblack_markdown.example_google]

Something else
"""
    extension = AutodocExtension(class_from_init=True)
    output = markdown.markdown(content, extensions=[extension])
    assert output is not None

def test_etree():
    tree = etree.fromstring('<div>Hello</div>')
    print(tree)
