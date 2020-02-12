# Configuration

The configuration parameters can be specified in the `mkdocs.yml` file:

```yaml
markdown_extensions:
  - admonition
  - codehilite
  - jetblack_markdown.autodoc:
      class_from_init: true
      ignore_dunder: true
      ignore_private: true
      ignore_all: false
      prefer_docstring: true
      template_file: black.jinja2
      template_folder: /usr/local/share/jetblack-markdown
```

## **class_from_init** (*bool, optional*) = `true`

If `true` use the docstring from the &#95;&#95;init&#95;&#95; function for
classes when generating the documentation for the constructor; otherwise use
the docstring from the class. e.g.

```python
class MyClass:
    """A simple class.

    If class_from_init == false use this docstring.

    Arguments:
        name (str): The name
    """

    def __init__(self, name: str):
        """A simple class.

        If class_from_init == true use this docstring.

        Arguments:
            name (str): The name

        self.name = name
```

## **ignore_dunder** (*bool, optional*) = `true`

If `true` ignore &#95;&#95;XXX&#95;&#95; functions.

## **ignore_private** (*bool, optional*) = `true`

If `true` ignore methods (those prefixed &#95;XXX).

## **ignore_all** (*bool, optional*) = `false`

If `false` use the &#95;&#95;all&#95;&#95; member to constrain which objects
are documented.

## **ignore_inherited** (*bool, optional*) = `true`

If `true` ignore inherited members.

## **prefer_docstring** (*bool, optional*) = `true`

If `true` prefer the docstring over the typing and inspection. This can be useful
in reducing the verboseness of the output, and providing symbolic defaults rather
than literal defaults. e.g.

```python
SomeType = Optional[Union[str, int]]
SOME_DEFAULT = "This is not a test"

def some_func(arg: SomeType = SOME_DEFAULT) -> None:
    """Some function
    
    Arguments:
        arg (SomeType): an argument
    """
    pass
```

If `prefer_docstring` is `true` this would provide:

```python
def some_func(arg: SomeType = SOME_DEFAULT) -> None:
```


But if `prefer_docstring` is `false`:

```python
def some_func(arg: Union[str, int, NoneType] = "This is not a test") -> None:
```

## **follow_module_tree** (*bool, optional*) = `false`

If `true` explore the module tree javadoc style. This is most useful when
combined with `ignore_all` = `false`.

## **template_file** (*Optional[str], optional*) = `"main.jinja2"`

The name of the template file to run.

## **template_folder** (*Optional[str], optional*) = `None`

The folder in which the templates can be found. If this is not specified the
built in templates are used.