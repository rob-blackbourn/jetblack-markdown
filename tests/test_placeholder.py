"""A test placeholder"""


import markdown

from jetblack_markdown.autodoc import AutodocExtension


def test_placeholder():
    content = """

@[jetblack_markdown.example_google:ExampleClass]

Something else
"""
    output = markdown.markdown(content, extensions=[AutodocExtension(class_from_init=True)])
    assert output is not None
