"""A test placeholder"""


import markdown


def test_placeholder():
    content = """

@[jetblack_markdown.example_google.example_generator]

Something else
"""
    output = markdown.markdown(content, extensions=["jetblack_markdown.autodoc"])
    assert output is not None
