# Welcome

Markdown extensions for [mkdocs](https://www.mkdocs.org/).

## Autodoc Extension

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

### mkdocs integration

This site was generated using `mkdocs` and the following config:

```yaml
site_name: jetblack-markdown

docs_dir: documentation
site_dir: docs

markdown_extensions:
  - admonition
  - codehilite
  - jetblack_markdown.autodoc:
      ignore_all: false
      ignore_inherited: true
      prefer_docstring: true
      follow_module_tree: False

extra_css:
    - css/custom.css
```

### Customizing

All the rendering is done with jinja2 templates. Start by copying the current
templates from jetblack_markdown/templates and specify the `template_folder` in
the `mkdocs.yml`.

## Latex2MathML Extension

A markdown extension is provided for converting LaTex style math formula
to MathML. This uses the [latex2mathml](https://github.com/roniemartinez/latex2mathml)
package.

An inline formula looks like: $d_1 = \frac{\ln(F/K) + (\sigma^2/2)T}{\sigma\sqrt{T}}$.

A block looks like:

$$
d_1 = \frac{\ln(F/K) + (\sigma^2/2)T}{\sigma\sqrt{T}}
$$

The outer `<math>` tag has the HTML class `"latex2mathml"`.

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
      ignore_all: false
      ignore_inherited: true
      prefer_docstring: true
      follow_module_tree: False
  - jetblack_markdown.latex2mathml:

extra_css:
    - css/custom.css
```
