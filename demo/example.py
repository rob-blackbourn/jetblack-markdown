import markdown
from jetblack_markdown import AutodocExtension

if __name__ == "__main__":
    content = """

# autodoc

@[jetblack_markdown]

"""
    extension = AutodocExtension(class_from_init=True, follow_module_tree=True)
    output = markdown.markdown(
        content, extensions=[
            "admonition",
            "codehilite",
            extension,
        ])
    print(output)
    assert output is not None
