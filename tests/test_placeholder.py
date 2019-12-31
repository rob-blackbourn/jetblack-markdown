"""A test placeholder"""


import markdown


def test_placeholder():
    content = """
This ??is some?? markdown.

@[jetblack_markdown.myextension.sample_func]

Something else
"""
    output = markdown.markdown(content, extensions=["jetblack_markdown"])
    assert output is not None
