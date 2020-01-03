"""A test placeholder"""


import markdown


def test_placeholder():
    content = """

@[jetblack_markdown.example_google:module_level_function]

Something else
"""
    output = markdown.markdown(content, extensions=["jetblack_markdown.autodoc"])
    assert output is not None
