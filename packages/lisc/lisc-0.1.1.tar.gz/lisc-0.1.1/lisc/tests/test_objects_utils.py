"""Tests for the objects utilities."""

from lisc.objects.utils import *

###################################################################################################
###################################################################################################

def test_wrap():

    assert wrap('string') == "'string'"

def test_get_max_length():

    assert get_max_length(['aa', 'aaa', 'a']) == 3
    assert get_max_length([1, 123, 12, 1234]) == 4
    assert get_max_length(['aa', 'a'], 2) == 4
