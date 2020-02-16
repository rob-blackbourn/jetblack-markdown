"""Tests for callables.py"""

from jetblack_markdown.metadata.callables import CallableDescriptor

from ..mocks import mock_func, mock_func_with_kwargs, DEFAULT_INT


def test_default():
    """A test for raises"""
    callable_desc = CallableDescriptor.create(mock_func, prefer_docstring=True)
    assert callable_desc.arguments[1].default == 'DEFAULT_INT'
    callable_desc = CallableDescriptor.create(
        mock_func, prefer_docstring=False)
    assert callable_desc.arguments[1].default == DEFAULT_INT


def test_kwargs():
    """A test for keyword args"""
    callable_desc = CallableDescriptor.create(
        mock_func_with_kwargs, prefer_docstring=True
    )
    assert callable_desc
