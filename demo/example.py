import markdown
from jetblack_markdown import AutodocExtension

if __name__ == "__main__":
    content = """

@[jetblack_markdown.metadata:ClassDescriptor]

Something else
"""
    extension = AutodocExtension(class_from_init=True)
    output = markdown.markdown(content, extensions=[extension])
    assert output is not None
