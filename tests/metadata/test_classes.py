"""Tests for callables.py"""

from jetblack_markdown.metadata.classes import ClassDescriptor

from ..mocks import MockClass, MockNamedTuple


def test_default():
    """A test for raises"""
    class_desc = ClassDescriptor.create(MockClass, True, True, True, True)
    assert class_desc

def test_named_tuple():
    """Test for NamedTuple"""
    class_desc = ClassDescriptor.create(MockNamedTuple, True, True, True, True)
    assert class_desc
