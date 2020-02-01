"""Tests for callables.py"""

from jetblack_markdown.metadata.classes import ClassDescriptor

from ..mocks import MockClass


def test_default():
    """A test for raises"""
    class_desc = ClassDescriptor.create(MockClass, True, True, True)
    assert class_desc
