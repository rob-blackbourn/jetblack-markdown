# Docstrings

The automatic documentation will use docstrings do enhance the documentation.
As this is a markdown extension, markdown an be used in the docstrings.

```python
def makeExtension(*args, **kwargs) -> Extension:
    """Make the extension

    This hook *function* gets picked up by the markdown processor when the
    extension is listed

    ```python
    output = markdown.markdown(
        content, extensions=[
            "admonition",
            "codehilite",
            "jetblack_markdown.autodoc",
        ])
    print(output)
    ```

    Returns:
        Extension: The extension
    """
    return AutodocExtension(*args, **kwargs)
```

Note the markdown on `function`, and the python code block.

Docstrings are parsed with the [docstrings_parser](https://github.com/rr-/docstring_parser).
This has been tested only with Google style docstrings.
