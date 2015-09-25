import pytest
from opendoor_listings.helpers import check_input, check_max_min

# Test check_input
def test_check_input():
    assert check_input('1.56') == False
    assert check_input('-1') == False
    assert check_input('2') == True

# Test check_max_min
def test_check_max_min():
    assert check_max_min(500, 1000) == False
    assert check_max_min(5000, 1000) == True
