"""Tests on utils.py"""

from jetblack_markdown.metadata.utils import is_named_tuple_type

from ..mocks import MockNamedTuple, MockClass, mock_func


def test_is_named_tuple():
    """Test for is_named_tuple"""
    assert is_named_tuple_type(MockNamedTuple)
    assert not is_named_tuple_type(MockClass)
    assert not is_named_tuple_type(mock_func)
