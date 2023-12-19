import markdown
from markdown.extensions.md_in_html import MarkdownInHtmlExtension

from jetblack_markdown import AutodocExtension, Latex2MathMLExtension

if __name__ == "__main__":
    content = """

# autodoc

* Item *one*.
* Item **two**.

@[jetblack_markdown.latex2mathml]

"""
    extensions = [
        MarkdownInHtmlExtension(),
        AutodocExtension(class_from_init=True, follow_module_tree=True),
        Latex2MathMLExtension()
    ]
    output = markdown.markdown(content, extensions=extensions)
    print(output)
    assert output is not None
