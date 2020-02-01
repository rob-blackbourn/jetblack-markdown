import markdown
from jetblack_markdown import AutodocExtension

if __name__ == "__main__":
    content = """

@[jetblack_markdown.autodoc:makeExtension]

Something else

```python
import foo

print(foo)
```
"""
    extension = AutodocExtension(class_from_init=True)
    output = markdown.markdown(
        content, extensions=[
            "admonition",
            "codehilite",
            "jetblack_markdown.autodoc",
        ])
    print(output)
    assert output is not None
