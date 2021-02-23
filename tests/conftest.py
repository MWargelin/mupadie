import pytest

@pytest.fixture
def unsorted_point_set():
    """Returns simple, unsorted point set"""
    return [(3,2), (1,3), (2,2), (2,1), (2,3), (1,1)]


@pytest.fixture
def sorted_point_set():
    """Returns simple, unsorted point set"""
    return [(1,1), (1,3), (2,1), (2,2), (2,3), (3,2)]
