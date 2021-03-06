# Templates

[Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templating
is used to render the documentation.

## The entry point

The template file is passed an `obj` parameter which is of type
`jetblack_markdown.metadata.Descriptor`. The descriptor has a type property.
The default template file looks like this:

```python
{% import 'macros.jinja2' as macros with context %}
{% if obj.descriptor_type == "module" %}
{{ macros.render_module(obj) }}
{% elif obj.descriptor_type == "class" %}
{{ macros.render_class(obj) }}
{% elif obj.descriptor_type == "callable" %}
{{ macros.render_callable(obj) }}
{% endif %}
```

It renders the appropriate template by checking the type
of the descriptor and then calling a macro.

## A renderer

Here's a simple render macro for rendering the "Summary" which is usually the
long description from the docstring.

```python
{% macro render_summary(summary) -%}
{% if summary -%}
  <h4 class="autodoc-title">Summary</h4>
  {{ summary | md_format }}
{%- endif %}
{%- endmacro %}
```

First it checks if the long description has been specified. If it has it renders
it as a level 4 heading with the class `autodoc-title`. Finally it uses a built
in custom filter to convert the docstring to markdown. The custom filter will
generate it's contents in a `<p> ... </p>` block.

Here's a more complex example of rendering a signature.

```python
{% macro render_signature(callable) -%}
<code class="autodoc-signature">
    {%- if callable.is_async -%}
    <span class="autodoc-keyword">async</span><span> </span>
    {%- endif -%}
    <span class="autodoc-qualifier">{{ callable.qualifier }}</span><span class="autodoc-punctuation">.</span><var class="autodoc-varname">{{ callable.name }}</var><span class="autodoc-punctuation">(</span>
    {%- for arg in callable.arguments -%}
      {%- if not loop.first -%}
        <span class="autodoc-punctuation">, </span>
      {%- endif -%}
      <var class="autodoc-varname">{{ arg.name }}</var>
      {%- if arg.type -%}
        <span class="autodoc-punctuation">: </span><span class="autodoc-vartype">{{ arg.type }}</span>
      {%- endif -%}
    {%- endfor -%}
    <span class="autodoc-punctuation">)</span>
    {%- if return_type -%}
      <span class="autodoc-punctuation"> -&gt; </span><span class="autodoc-vartype">{{ return_type }}</span>
    {%- endif -%}
</code>
{%- endmacro %}
```

## The md_format filter

A custom filter `md_format` has been provided to process code that may contain markdown, such as the summary.

Here's an example of its use.

```python
{% macro render_summary(summary) -%}
{% if summary -%}
  <h4 class="autodoc-title">Summary</h4>
  {{ summary | md_format }}
{%- endif %}
{%- endmacro %}
```
