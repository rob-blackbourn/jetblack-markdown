# Configuration

There are some configuration parameters.

* **class_from_init** (*bool, optional*): If `true` use the docstring from
    the &#95;&#95;init&#95;&#95; function for classes. Defaults to
    `true`.
* **ignore_dunder** (*bool, optional*): If `true` ignore
    &#95;&#95;XXX&#95;&#95; functions. Defaults to `true`.
* **ignore_private** (*bool, optional*): If `true` ignore methods
    (those prefixed &#95;XXX). Defaults to `true`.
* **ignore_all** (*bool, optional*): If `true` ignore the &#95;&#95;all&#95;&#95; member.
    Defaults to `false`.
* **ignore_inherited** (*bool, optional*): If `true` ignore inherited members.
    Defaults to `true`
* **prefer_docstring** (*bool, optional*): If `true` prefer the docstring.
    Defaults to `true`
* **follow_module_tree** (*bool, optional*): If `true` follow the module tree.
    Defaults to `false`
* **template_folder** (*Optional[str], optional*): Specify a custom template folder.
    The template `main.jinja2` will be rendered passing an `obj` parameter
    which is a `jetblack.markdown.metadata.Descriptor`
