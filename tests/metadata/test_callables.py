"""Tests for callables.py"""

from jetblack_markdown.metadata.callables import CallableDescriptor

from ..mocks import mock_func, DEFAULT_INT


def test_default():
    """A test for raises"""
    callable_desc = CallableDescriptor.create(mock_func, prefer_docstring=True)
    assert callable_desc.arguments[1].default == 'DEFAULT_INT'
    callable_desc = CallableDescriptor.create(mock_func, prefer_docstring=False)
    assert callable_desc.arguments[1].default == DEFAULT_INT
