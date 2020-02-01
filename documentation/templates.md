# Templates

[Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templating
is used to render the documentation.

The template `main.jinja2` is passed an `obj` parameter which is of type `jetblack_markdown.metadata.Descriptor`.
The descriptor has a type. The default template libraries `main.jinja2` looks like this:

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
