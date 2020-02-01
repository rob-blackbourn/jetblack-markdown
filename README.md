# jetblack-markdown

Markdown extensions for automatic document generation.

See [here](https://rob-blackbourn.github.io/jetblack-markdown/) for documentation.

## Markdown Extension

A markdown extension is provided for automatically documenting python code.

Modules are referred to as follows:

```markdown
# A Top Level Module

@[jetblack_markdown]

# A Package

@[jetblack_markdown.autodoc]

# A function

@[jetblack_markdown.autodoc:makeExtension]

# A class

@[jetblack_markdown.autodoc.metadata:PropertyDescriptor]
```

## mkdocs integration

This site was generated using `mkdocs` and the following config:

```yaml
site_name: jetblack-markdown

docs_dir: documentation
site_dir: docs

markdown_extensions:
  - admonition
  - codehilite
  - jetblack_markdown.autodoc:
      class_from_init: true
      ignore_dunder: true
      ignore_private: true
      ignore_all: false
      prefer_docstring: true
      template_folder: null

extra_css:
    - css/custom.css
```

### Configuration

There are some configuration parameters.

* class_from_init (bool, optional): If True use the docstring from
    the &#95;&#95;init&#95;&#95; function for classes. Defaults to
    True.
* ignore_dunder (bool, optional): If True ignore
    &#95;&#95;XXX&#95;&#95; functions. Defaults to True.
* ignore_private (bool, optional): If True ignore methods
    (those prefixed &#95;XXX). Defaults to True.
* ignore_all (bool): If True ignore the &#95;&#95;all&#95;&#95; member.
* prefer_docstring (bool): If true prefer the docstring.
* template_folder(Optional[str], optional): Specify a custom template folder.
    The template "main.jinja2" will be rendered passing an `obj` parameter
    which is a `jetblack.markdown.metadata.Descriptor`

## Customizing

All the rendering is done with jinja2 templates. Start by copying the current
templates from jetblack_markdown/templates and specify the `template_folder` in
the `mkdocs.yml`.

