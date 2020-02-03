# Welcome

Markdown extensions for [mkdocs](https://www.mkdocs.org/).

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
      ignore_inherited: true
      prefer_docstring: true
      follow_module_tree: False
      template_folder: null

extra_css:
    - css/custom.css
```

## Customizing

All the rendering is done with jinja2 templates. Start by copying the current
templates from jetblack_markdown/templates and specify the `template_folder` in
the `mkdocs.yml`.
